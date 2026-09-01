from datetime import datetime, timezone

from bson import ObjectId
from fastapi.encoders import jsonable_encoder


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

class StockMovementRepository:

    def __init__(self, db):

        self.db = db


    # ==========================================
    # Create Movement
    # ==========================================

    async def create_movement(
        self,
        movement_data: dict
    ):

        safe_data = jsonable_encoder(
            movement_data
        )

        result = await self.db.stock_movements.insert_one(
            safe_data
        )

        return result.inserted_id


    # ==========================================
    # Get By Movement ID
    # ==========================================

    async def get_by_movement_id(

        self,
        hospital_id: str,
        movement_id: str

    ):

        movement = await self.db.stock_movements.find_one({

            "hospital_id": hospital_id,

            "movement_id": movement_id

        })

        return serialize_mongo_doc(
            movement
        )


    # ==========================================
    # Get Stock Movement History
    # ==========================================

    async def get_by_stock_id(

        self,
        hospital_id: str,
        stock_id: str

    ):

        movements = await self.db.stock_movements.find({

            "hospital_id": hospital_id,

            "stock_id": stock_id

        }).sort(

            "created_at",
            -1

        ).to_list(

            length=None

        )

        return [

            serialize_mongo_doc(movement)

            for movement in movements

        ]


    # ==========================================
    # Get By Reference
    # ==========================================

    async def get_by_reference(

        self,
        hospital_id: str,
        reference_type: str,
        reference_id: str

    ):

        movements = await self.db.stock_movements.find({

            "hospital_id": hospital_id,

            "reference_type": reference_type,

            "reference_id": reference_id

        }).sort(

            "created_at",
            -1

        ).to_list(

            length=None

        )

        return [

            serialize_mongo_doc(movement)

            for movement in movements

        ]


    # ==========================================
    # Get All Movements
    # ==========================================

    async def get_all_movements(

        self,
        hospital_id: str,
        page: int = 1,
        limit: int = 20,
        stock_id: str | None = None,
        medicine_id: str | None = None,
        batch_id: str | None = None,
        movement_type=None

    ):

        query = {

            "hospital_id": hospital_id

        }


        if stock_id:

            query["stock_id"] = stock_id


        if medicine_id:

            query["medicine_id"] = medicine_id


        if batch_id:

            query["batch_id"] = batch_id


        if movement_type:

            query["movement_type"] = movement_type.value


        total = await self.db.stock_movements.count_documents(
            query
        )


        skip = (page - 1) * limit


        movements = await self.db.stock_movements.find(
            query
        ).sort(
            "created_at",
            -1
        ).skip(
            skip
        ).limit(
            limit
        ).to_list(
            length=limit
        )


        return {

            "items": [

                serialize_mongo_doc(movement)

                for movement in movements

            ],

            "total": total

        }