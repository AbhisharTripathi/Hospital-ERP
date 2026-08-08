from datetime import datetime, timezone

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.models.medicine import MedicineUnit, DosageForm


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

class MedicineRepository:

    def __init__(self, db):

        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_medicine(
        self,
        medicine_data: dict
    ):

        safe_data = jsonable_encoder(
            medicine_data
        )

        result = await self.db.medicines.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Medicine ID
    # ==========================================

    async def get_by_medicine_id(

        self,
        hospital_id: str,
        medicine_id: str

    ):

        medicine = await self.db.medicines.find_one({

            "hospital_id": hospital_id,

            "medicine_id": medicine_id

        })

        return serialize_mongo_doc(
            medicine
        )

    # ==========================================
    # Check Duplicate Medicine
    # ==========================================

    async def find_duplicate(

        self,

        hospital_id: str,

        medicine_name: str,

        generic_name: str | None,

        strength: str | None,

        dosage_form: DosageForm,

        manufacturer: str | None

    ):

        query = {

            "hospital_id": hospital_id,

            "medicine_name": medicine_name,

            "strength": strength,

            "dosage_form": dosage_form,

            "manufacturer": manufacturer

        }

        if generic_name is not None:

            query["generic_name"] = generic_name

        medicine = await self.db.medicines.find_one(
            query
        )

        return serialize_mongo_doc(
            medicine
        )

    # ==========================================
    # Search / Autocomplete
    # ==========================================

    async def search_medicines(

        self,

        hospital_id: str,

        search: str,

        limit: int = 10

    ):

        query = {

            "hospital_id": hospital_id,

            "is_active": True,

            "$or": [

                {

                    "medicine_name": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "generic_name": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "strength": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        }

        medicines = await self.db.medicines.find(
            query
        ).sort(
            "medicine_name",
            1
        ).limit(
            limit
        ).to_list(
            length=limit
        )

        return [

            serialize_mongo_doc(item)

            for item in medicines

        ]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_medicines(

        self,

        hospital_id: str,

        page: int,

        limit: int,

        search: str | None,

        dosage_form: DosageForm | None,

        manufacturer: str | None,

        is_active: bool | None,

        sort_by: str,

        sort_order: int

    ):

        query = {

            "hospital_id": hospital_id

        }

        if search:

            query["$or"] = [

                {

                    "medicine_name": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "generic_name": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        if dosage_form:

            query["dosage_form"] = dosage_form

        if manufacturer:

            query["manufacturer"] = {

                "$regex": manufacturer,

                "$options": "i"

            }

        if is_active is not None:

            query["is_active"] = is_active

        total = await self.db.medicines.count_documents(
            query
        )

        skip = (page - 1) * limit

        medicines = await self.db.medicines.find(
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

                serialize_mongo_doc(item)

                for item in medicines

            ],

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_medicine(

        self,

        hospital_id: str,

        medicine_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = (
            datetime.now(timezone.utc)
        )

        safe_data = jsonable_encoder(
            update_data
        )

        return await self.db.medicines.update_one(

            {

                "hospital_id": hospital_id,

                "medicine_id": medicine_id

            },

            {

                "$set": safe_data

            }

        )

    # ==========================================
    # Update Active Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        medicine_id: str,

        is_active: bool

    ):

        return await self.db.medicines.update_one(

            {

                "hospital_id": hospital_id,

                "medicine_id": medicine_id

            },

            {

                "$set": {

                    "is_active": is_active,

                    "updated_at": (
                        datetime.now(timezone.utc)
                    )

                }

            }

        )