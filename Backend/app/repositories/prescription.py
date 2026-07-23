from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder
from app.models.prescription import PrescriptionStatus
from bson import ObjectId
def serialize_mongo_doc(doc: dict) -> dict:
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
                    serialize_mongo_doc(item) if isinstance(item, dict) 
                    else (str(item) if isinstance(item, ObjectId) else item)
                    for item in value
                ]
            else:
                cleaned[key] = value
        return cleaned
class PrescriptionRepository:

    def __init__(self, db):
        self.db = db

  
    # ==========================================
    # Create
    # ==========================================

    async def create_prescription(
        self,
        prescription_data: dict
    ):
        safe_data = jsonable_encoder(prescription_data)

        result = await self.db.prescriptions.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Prescription ID
    # ==========================================

    async def get_by_prescription_id(
        self,
        hospital_id: str,
        prescription_id: str
    ):
        prescription = await self.db.prescriptions.find_one({
            "prescription_id": prescription_id,
            "hospital_id": hospital_id
        })
        return serialize_mongo_doc(prescription)

    # ==========================================
    # Get By Appointment
    # ==========================================

    async def get_by_appointment_id(
        self,
        hospital_id: str,
        appointment_id: str
    ):
        prescription = await self.db.prescriptions.find_one({
            "hospital_id": hospital_id,
            "appointment_id": appointment_id
        })
        return serialize_mongo_doc(prescription)
        

    # ==========================================
    # Get Patient Prescriptions
    # ==========================================

    async def get_by_patient(
        self,
        hospital_id: str,
        patient_id: str
    ):

        cursor = self.db.prescriptions.find(

            {
                "hospital_id": hospital_id,
                "patient_id": patient_id
            }

        ).sort(
            "created_at",
            -1
        )
        prescriptions = await cursor.to_list(length=None)
        return [serialize_mongo_doc(p) for p in prescriptions]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_prescriptions(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: PrescriptionStatus | None = None,

        sort_by: str = "created_at",

        sort_order: int = -1

    ):

        query = {

            "hospital_id": hospital_id

        }

        if doctor_id:
            query["doctor_id"] = doctor_id

        if patient_id:
            query["patient_id"] = patient_id

        if status:
            query["status"] = status

        if search:

            query["$or"] = [

                {
                    "prescription_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "diagnosis": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.prescriptions.count_documents(
            query
        )

        skip = (page - 1) * limit

        prescriptions = await self.db.prescriptions.find(
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

        serialized_prescriptions = [serialize_mongo_doc(p) for p in prescriptions]
        return {

            "items": serialized_prescriptions,

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_prescription(

        self,

        hospital_id: str,

        prescription_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )
        safe_update_data = jsonable_encoder(update_data)

        return await self.db.prescriptions.update_one(

            {
                "hospital_id": hospital_id,
                "prescription_id": prescription_id
            },

            {
                "$set": safe_update_data
            }

        )

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        prescription_id: str,

        status: PrescriptionStatus

    ):

        return await self.db.prescriptions.update_one(

            {
                "hospital_id": hospital_id,
                "prescription_id": prescription_id
            },

            {
                "$set": {

                    "status": status.value,

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }
            }

        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete_prescription(

        self,

        hospital_id: str,

        prescription_id: str

    ):

        return await self.db.prescriptions.delete_one(

            {
                "hospital_id": hospital_id,
                "prescription_id": prescription_id
            }

        )

