from datetime import datetime, timezone

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.models.pharmacy import PharmacyStatus


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

class PharmacyRepository:

    def __init__(self, db):

        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_pharmacy(self, pharmacy_data: dict):

        safe_data = jsonable_encoder(pharmacy_data)

        result = await self.db.pharmacy.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Pharmacy ID
    # ==========================================

    async def get_by_pharmacy_id(

        self,

        hospital_id: str,

        pharmacy_id: str

    ):

        pharmacy = await self.db.pharmacy.find_one({

            "hospital_id": hospital_id,

            "pharmacy_id": pharmacy_id

        })

        return serialize_mongo_doc(pharmacy)

    # ==========================================
    # Get By Prescription
    # ==========================================

    async def get_by_prescription_id(

        self,

        hospital_id: str,

        prescription_id: str

    ):

        pharmacy = await self.db.pharmacy.find_one({

            "hospital_id": hospital_id,

            "prescription_id": prescription_id

        })

        return serialize_mongo_doc(pharmacy)

    # ==========================================
    # Get By Patient
    # ==========================================

    async def get_by_patient(

        self,

        hospital_id: str,

        patient_id: str

    ):

        cursor = self.db.pharmacy.find({

            "hospital_id": hospital_id,

            "patient_id": patient_id

        }).sort(

            "created_at",

            -1

        )

        pharmacies = await cursor.to_list(length=None)

        return [

            serialize_mongo_doc(item)

            for item in pharmacies

        ]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_pharmacy(

        self,

        hospital_id: str,

        page: int,

        limit: int,

        search: str | None,

        patient_id: str | None,

        doctor_id: str | None,

        pharmacist_id: str | None,

        status: PharmacyStatus | None,

        sort_by: str,

        sort_order: int

    ):

        query = {

            "hospital_id": hospital_id

        }

        if patient_id:

            query["patient_id"] = patient_id

        if doctor_id:

            query["doctor_id"] = doctor_id

        if pharmacist_id:

            query["pharmacist_id"] = pharmacist_id

        if status:

            query["status"] = status

        if search:

            query["$or"] = [

                {

                    "pharmacy_id": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "prescription_id": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        total = await self.db.pharmacy.count_documents(query)

        skip = (page - 1) * limit

        pharmacies = await self.db.pharmacy.find(

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

                for item in pharmacies

            ],

            "total": total

        }

    # ==========================================
    # Update Medicines
    # ==========================================

    async def update_pharmacy(

        self,

        hospital_id: str,

        pharmacy_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        safe_data = jsonable_encoder(update_data)

        return await self.db.pharmacy.update_one(

            {

                "hospital_id": hospital_id,

                "pharmacy_id": pharmacy_id

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

        pharmacy_id: str,

        status: PharmacyStatus,

        pharmacist_id: str

    ):

        return await self.db.pharmacy.update_one(

            {

                "hospital_id": hospital_id,

                "pharmacy_id": pharmacy_id

            },

            {

                "$set": {

                    "status": status.value,

                    "pharmacist_id": pharmacist_id,

                    "dispensed_at": datetime.now(
                        timezone.utc
                    ),

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }

            }

        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete_pharmacy(

        self,

        hospital_id: str,

        pharmacy_id: str

    ):

        return await self.db.pharmacy.delete_one({

            "hospital_id": hospital_id,

            "pharmacy_id": pharmacy_id

        })