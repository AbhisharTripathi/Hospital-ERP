from datetime import (
    datetime,
    timezone
)

from bson import ObjectId

from fastapi.encoders import jsonable_encoder

from app.models.consultation import (
    ConsultationStatus
)


# ==========================================
# Mongo Serializer
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

class ConsultationRepository:

    def __init__(

        self,

        db

    ):

        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_consultation(

        self,

        consultation_data: dict

    ):

        safe_data = jsonable_encoder(
            consultation_data
        )

        result = await self.db.consultations.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Consultation ID
    # ==========================================

    async def get_by_consultation_id(

        self,

        hospital_id: str,

        consultation_id: str

    ):

        consultation = await self.db.consultations.find_one(

            {

                "hospital_id": hospital_id,

                "consultation_id": consultation_id

            }

        )

        return serialize_mongo_doc(
            consultation
        )

    # ==========================================
    # Get By Appointment
    # ==========================================

    async def get_by_appointment_id(

        self,

        hospital_id: str,

        appointment_id: str

    ):

        consultation = await self.db.consultations.find_one(

            {

                "hospital_id": hospital_id,

                "appointment_id": appointment_id

            }

        )

        return serialize_mongo_doc(
            consultation
        )

    # ==========================================
    # Get Patient Consultation History
    # ==========================================

    async def get_by_patient(

        self,

        hospital_id: str,

        patient_id: str

    ):

        cursor = self.db.consultations.find(

            {

                "hospital_id": hospital_id,

                "patient_id": patient_id

            }

        ).sort(

            "created_at",

            -1

        )

        consultations = await cursor.to_list(
            length=None
        )

        return [

            serialize_mongo_doc(c)

            for c in consultations

        ]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_consultations(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: ConsultationStatus | None = None,

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

                    "consultation_id": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "diagnosis": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "chief_complaint": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        total = await self.db.consultations.count_documents(
            query
        )

        skip = (page - 1) * limit

        consultations = await self.db.consultations.find(

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

                serialize_mongo_doc(c)

                for c in consultations

            ],

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_consultation(

        self,

        hospital_id: str,

        consultation_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        safe_update = jsonable_encoder(
            update_data
        )

        return await self.db.consultations.update_one(

            {

                "hospital_id": hospital_id,

                "consultation_id": consultation_id

            },

            {

                "$set": safe_update

            }

        )

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        consultation_id: str,

        status: ConsultationStatus

    ):

        return await self.db.consultations.update_one(

            {

                "hospital_id": hospital_id,

                "consultation_id": consultation_id

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

    async def delete_consultation(

        self,

        hospital_id: str,

        consultation_id: str

    ):

        return await self.db.consultations.delete_one(

            {

                "hospital_id": hospital_id,

                "consultation_id": consultation_id

            }

        )