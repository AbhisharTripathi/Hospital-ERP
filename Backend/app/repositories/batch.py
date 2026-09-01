
from datetime import datetime, date, time, timezone
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

class BatchRepository:

    def __init__(self, db):

        self.db = db

    # ==========================================
    # Create Batch
    # ==========================================

    async def create_batch(
        self,
        batch_data: dict
    ):

        safe_data = jsonable_encoder(
            batch_data
        )

        result = await self.db.batches.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Batch ID
    # ==========================================

    async def get_by_batch_id(

        self,
        hospital_id: str,
        batch_id: str

    ):

        batch = await self.db.batches.find_one({

            "hospital_id": hospital_id,

            "batch_id": batch_id

        })

        return serialize_mongo_doc(batch)

    # ==========================================
    # Find Medicine Batch
    # ==========================================

    async def find_by_medicine_and_batch(

        self,
        hospital_id: str,
        medicine_id: str,
        batch_number: str

    ):

        batch = await self.db.batches.find_one({

            "hospital_id": hospital_id,

            "medicine_id": medicine_id,

            "batch_number": batch_number

        })

        return serialize_mongo_doc(batch)

    # ==========================================
    # Get Batches By Medicine
    # ==========================================

    async def get_by_medicine(

        self,
        hospital_id: str,
        medicine_id: str

    ):

        cursor = self.db.batches.find({

            "hospital_id": hospital_id,

            "medicine_id": medicine_id

        }).sort(

            "expiry_date",
            1

        )

        batches = await cursor.to_list(
            length=None
        )

        return [
            serialize_mongo_doc(batch)
            for batch in batches
        ]

    # ==========================================
    # Get All Batches
    # ==========================================

    async def get_all_batches(

        self,
        hospital_id: str,
        page: int,
        limit: int,
        medicine_id: str | None = None,
        status=None,
        sort_by: str = "expiry_date",
        sort_order: int = 1

    ):

        query = {

            "hospital_id": hospital_id

        }

        if medicine_id:

            query["medicine_id"] = medicine_id

        if status:

            query["status"] = status

        total = await self.db.batches.count_documents(
            query
        )

        skip = (page - 1) * limit

        batches = await self.db.batches.find(
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

                serialize_mongo_doc(batch)

                for batch in batches

            ],

            "total": total

        }

    # ==========================================
    # Update Batch
    # ==========================================

    async def update_batch(

        self,
        hospital_id: str,
        batch_id: str,
        update_data: dict

    ):

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        safe_data = jsonable_encoder(
            update_data
        )

        return await self.db.batches.update_one(

            {

                "hospital_id": hospital_id,

                "batch_id": batch_id

            },

            {

                "$set": safe_data

            }

        )

    # ==========================================
    # Get Expired Batches
    # ==========================================

    async def get_expired_batches(
        self,
        hospital_id: str,
        today
    ):
        # Agar 'today' datetime.date object hai, to use datetime.datetime mein convert karein
        if isinstance(today, date) and not isinstance(today, datetime):
            today = datetime.combine(today, time.min)

        batches = await self.db.batches.find({
            "hospital_id": hospital_id,
            "expiry_date": {
                "$lt": today
            }
        }).to_list(
            length=None
        )

        return [
            serialize_mongo_doc(batch)
            for batch in batches
        ]