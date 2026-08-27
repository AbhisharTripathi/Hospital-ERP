from datetime import datetime, timezone

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.models.purchase import PurchaseStatus


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

class PurchaseRepository:

    def __init__(self, db):

        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_purchase(
        self,
        purchase_data: dict
    ):

        safe_data = jsonable_encoder(
            purchase_data
        )

        result = await self.db.purchases.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Purchase ID
    # ==========================================

    async def get_by_purchase_id(
        self,
        hospital_id: str,
        purchase_id: str
    ):

        purchase = await self.db.purchases.find_one({

            "hospital_id": hospital_id,

            "purchase_id": purchase_id

        })

        return serialize_mongo_doc(
            purchase
        )

    # ==========================================
    # Get By Invoice Number
    # ==========================================

    async def get_by_invoice_number(
        self,
        hospital_id: str,
        invoice_number: str
    ):

        purchase = await self.db.purchases.find_one({

            "hospital_id": hospital_id,

            "invoice_number": invoice_number

        })

        return serialize_mongo_doc(
            purchase
        )

    # ==========================================
    # Get By Supplier
    # ==========================================

    async def get_by_supplier(
        self,
        hospital_id: str,
        supplier_id: str
    ):

        cursor = self.db.purchases.find({

            "hospital_id": hospital_id,

            "supplier_id": supplier_id

        }).sort(

            "created_at",
            -1

        )

        purchases = await cursor.to_list(
            length=None
        )

        return [

            serialize_mongo_doc(
                purchase
            )

            for purchase in purchases

        ]

    # ==========================================
    # Get All Purchases
    # ==========================================

    async def get_all_purchases(

        self,

        hospital_id: str,

        page: int,

        limit: int,

        search: str | None,

        supplier_id: str | None,

        status: PurchaseStatus | None,

        sort_by: str,

        sort_order: int

    ):

        query = {

            "hospital_id": hospital_id

        }

        # --------------------------------------
        # Supplier Filter
        # --------------------------------------

        if supplier_id:

            query["supplier_id"] = supplier_id

        # --------------------------------------
        # Status Filter
        # --------------------------------------

        if status:

            query["status"] = status.value

        # --------------------------------------
        # Search
        # --------------------------------------

        if search:

            query["$or"] = [

                {

                    "purchase_id": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "invoice_number": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        # --------------------------------------
        # Total
        # --------------------------------------

        total = await self.db.purchases.count_documents(
            query
        )

        # --------------------------------------
        # Pagination
        # --------------------------------------

        skip = (page - 1) * limit

        purchases = await self.db.purchases.find(
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

                serialize_mongo_doc(
                    purchase
                )

                for purchase in purchases

            ],

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_purchase(

        self,

        hospital_id: str,

        purchase_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        safe_data = jsonable_encoder(
            update_data
        )

        return await self.db.purchases.update_one(

            {

                "hospital_id": hospital_id,

                "purchase_id": purchase_id

            },

            {

                "$set": safe_data

            }

        )

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        purchase_id: str,

        status: PurchaseStatus

    ):

        return await self.db.purchases.update_one(

            {

                "hospital_id": hospital_id,

                "purchase_id": purchase_id

            },

            {

                "$set": {

                    "status": status.value,

                    "updated_at":
                        datetime.now(timezone.utc)

                }

            }

        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete_purchase(

        self,

        hospital_id: str,

        purchase_id: str

    ):

        return await self.db.purchases.delete_one(

            {

                "hospital_id": hospital_id,

                "purchase_id": purchase_id

            }

        )