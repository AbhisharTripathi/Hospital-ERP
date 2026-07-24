from datetime import datetime, timezone

from fastapi.encoders import jsonable_encoder

from app.repositories.prescription import serialize_mongo_doc
from app.models.vitals import VitalStatus


class VitalRepository:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_vital(
        self,
        vital_data: dict
    ):

        vital_data = jsonable_encoder(
            vital_data
        )

        result = await self.db.vitals.insert_one(
            vital_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Vital ID
    # ==========================================

    async def get_by_vital_id(
        self,
        hospital_id: str,
        vital_id: str
    ):

        vital = await self.db.vitals.find_one(

            {
                "hospital_id": hospital_id,
                "vital_id": vital_id
            }

        )

        if not vital:
            return None

        return serialize_mongo_doc(
            vital
        )

    # ==========================================
    # Get By Appointment
    # ==========================================

    async def get_by_appointment(
        self,
        hospital_id: str,
        appointment_id: str
    ):

        vital = await self.db.vitals.find_one(

            {
                "hospital_id": hospital_id,
                "appointment_id": appointment_id
            }

        )

        if not vital:
            return None

        return serialize_mongo_doc(
            vital
        )

    # ==========================================
    # Patient Vitals History
    # ==========================================

    async def get_patient_vitals(
        self,
        hospital_id: str,
        patient_id: str
    ):

        cursor = self.db.vitals.find(

            {
                "hospital_id": hospital_id,
                "patient_id": patient_id
            }

        ).sort(

            "recorded_at",
            -1

        )

        vitals = await cursor.to_list(
            length=None
        )

        return [

            serialize_mongo_doc(v)
            for v in vitals

        ]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_vitals(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: VitalStatus | None = None,

        sort_by: str = "recorded_at",

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
                    "vital_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "patient_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "appointment_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.vitals.count_documents(
            query
        )

        skip = (page - 1) * limit

        vitals = await self.db.vitals.find(

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
                    vital
                )

                for vital in vitals

            ],

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_vital(

        self,

        hospital_id: str,

        vital_id: str,

        update_data: dict

    ):

        update_data = jsonable_encoder(
            update_data
        )

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        return await self.db.vitals.update_one(

            {
                "hospital_id": hospital_id,
                "vital_id": vital_id
            },

            {
                "$set": update_data
            }

        )

    # ==========================================
    # Update Status
    # ==========================================

    async def update_status(

        self,

        hospital_id: str,

        vital_id: str,

        status: VitalStatus

    ):

        return await self.db.vitals.update_one(

            {
                "hospital_id": hospital_id,
                "vital_id": vital_id
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

    async def delete_vital(

        self,

        hospital_id: str,

        vital_id: str

    ):

        return await self.db.vitals.delete_one(

            {
                "hospital_id": hospital_id,
                "vital_id": vital_id
            }

        )