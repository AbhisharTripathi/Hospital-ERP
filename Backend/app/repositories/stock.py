from datetime import datetime, timezone

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.models.stock import StockStatus


# ==========================================
# Serialize Mongo Document
# ==========================================

def serialize_mongo_doc(doc: dict):

    if not doc:
        return doc

    cleaned = {}

    for key, value in doc.items():

        if isinstance(value, ObjectId):

            cleaned[key] = str(value)

        elif isinstance(value, dict):

            cleaned[key] = serialize_mongo_doc(value)

        elif isinstance(value, list):

            cleaned[key] = [

                serialize_mongo_doc(item)
                if isinstance(item, dict)
                else (
                    str(item)
                    if isinstance(item, ObjectId)
                    else item
                )

                for item in value
            ]

        else:

            cleaned[key] = value

    return cleaned


# ==========================================
# Repository
# ==========================================

class StockRepository:

    def __init__(self, db):

        self.db = db


    # ==========================================
    # Create
    # ==========================================

    async def create_stock(
        self,
        stock_data: dict
    ):

        safe_data = jsonable_encoder(
            stock_data
        )

        result = await self.db.stocks.insert_one(
            safe_data
        )

        return result.inserted_id


    # ==========================================
    # Get By Stock ID
    # ==========================================

    async def get_by_stock_id(
        self,
        hospital_id: str,
        stock_id: str
    ):

        stock = await self.db.stocks.find_one({

            "hospital_id": hospital_id,

            "stock_id": stock_id

        })

        return serialize_mongo_doc(stock)


    # ==========================================
    # Get By Medicine + Batch
    # ==========================================

    async def get_by_medicine_batch(
        self,
        hospital_id: str,
        medicine_id: str,
        batch_id: str
    ):

        stock = await self.db.stocks.find_one({

            "hospital_id": hospital_id,

            "medicine_id": medicine_id,

            "batch_id": batch_id

        })

        return serialize_mongo_doc(stock)


    # ==========================================
    # Get Medicine Stock
    # ==========================================

    async def get_by_medicine(
        self,
        hospital_id: str,
        medicine_id: str
    ):

        cursor = self.db.stocks.find({

            "hospital_id": hospital_id,

            "medicine_id": medicine_id,

            "status": StockStatus.AVAILABLE.value

        }).sort(

            "updated_at",
            -1

        )

        stocks = await cursor.to_list(
            length=None
        )

        return [
            serialize_mongo_doc(stock)
            for stock in stocks
        ]


    # ==========================================
    # Get All Stock
    # ==========================================

    async def get_all_stock(

        self,
        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        medicine_id: str | None = None,

        batch_id: str | None = None,

        status: StockStatus | None = None,

        sort_by: str = "updated_at",

        sort_order: int = -1

    ):

        query = {

            "hospital_id": hospital_id

        }


        if medicine_id:

            query["medicine_id"] = medicine_id


        if batch_id:

            query["batch_id"] = batch_id


        if status:

            query["status"] = status.value


        total = await self.db.stocks.count_documents(
            query
        )


        skip = (page - 1) * limit


        stocks = await self.db.stocks.find(
            query
        ).sort(
            sort_by,
            sort_order
        ).skip(
            skip
        ).limit(
            limit
        ).to_list(
            length=limit
        )


        return {

            "items": [

                serialize_mongo_doc(stock)

                for stock in stocks

            ],

            "total": total

        }


    # ==========================================
    # Update Stock
    # ==========================================

    async def update_stock(

        self,
        hospital_id: str,
        stock_id: str,
        update_data: dict

    ):

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        safe_data = jsonable_encoder(
            update_data
        )

        return await self.db.stocks.update_one(

            {

                "hospital_id": hospital_id,

                "stock_id": stock_id

            },

            {

                "$set": safe_data

            }

        )


    # ==========================================
    # Increase Quantity
    # ==========================================

    async def increase_quantity(

        self,
        hospital_id: str,
        stock_id: str,
        quantity: int

    ):

        return await self.db.stocks.update_one(

            {

                "hospital_id": hospital_id,

                "stock_id": stock_id

            },

            {

                "$inc": {

                    "quantity": quantity,

                    "available_quantity": quantity

                },

                "$set": {

                    "updated_at":
                    datetime.now(timezone.utc)

                }

            }

        )


    # ==========================================
    # Decrease Quantity
    # ==========================================

    async def decrease_quantity(

        self,
        hospital_id: str,
        stock_id: str,
        quantity: int

    ):

        return await self.db.stocks.update_one(

            {

                "hospital_id": hospital_id,

                "stock_id": stock_id,

                "available_quantity": {
                    "$gte": quantity
                }

            },

            {

                "$inc": {

                    "quantity": -quantity,

                    "available_quantity": -quantity

                },

                "$set": {

                    "updated_at":
                    datetime.now(timezone.utc)

                }

            }

        )