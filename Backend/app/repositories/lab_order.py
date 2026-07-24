from datetime import (
    datetime,
    timezone
)

from bson import ObjectId

from fastapi.encoders import jsonable_encoder

from app.models.lab_order import (
    LabOrderStatus
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

class LabOrderRepository:

    def __init__(

        self,

        db

    ):

        self.db = db

    # ==========================================
    # Create
    # ==========================================

    async def create_lab_order(

        self,

        lab_order_data: dict

    ):

        safe_data = jsonable_encoder(
            lab_order_data
        )

        result = await self.db.lab_orders.insert_one(
            safe_data
        )

        return result.inserted_id

    # ==========================================
    # Get By Lab Order ID
    # ==========================================

    async def get_by_lab_order_id(

        self,

        hospital_id: str,

        lab_order_id: str

    ):

        lab_order = await self.db.lab_orders.find_one(

            {

                "hospital_id": hospital_id,

                "lab_order_id": lab_order_id

            }

        )

        return serialize_mongo_doc(
            lab_order
        )

    # ==========================================
    # Get By Appointment
    # ==========================================

    async def get_by_appointment_id(

        self,

        hospital_id: str,

        appointment_id: str

    ):

        lab_order = await self.db.lab_orders.find_one(

            {

                "hospital_id": hospital_id,

                "appointment_id": appointment_id

            }

        )

        return serialize_mongo_doc(
            lab_order
        )

    # ==========================================
    # Get Patient History
    # ==========================================

    async def get_by_patient(

        self,

        hospital_id: str,

        patient_id: str

    ):

        cursor = self.db.lab_orders.find(

            {

                "hospital_id": hospital_id,

                "patient_id": patient_id

            }

        ).sort(

            "created_at",

            -1

        )

        lab_orders = await cursor.to_list(
            length=None
        )

        return [

            serialize_mongo_doc(item)

            for item in lab_orders

        ]

    # ==========================================
    # Get All
    # ==========================================

    async def get_all_lab_orders(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: LabOrderStatus | None = None,

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

                    "lab_order_id": {

                        "$regex": search,

                        "$options": "i"

                    }

                },

                {

                    "clinical_notes": {

                        "$regex": search,

                        "$options": "i"

                    }

                }

            ]

        total = await self.db.lab_orders.count_documents(
            query
        )

        skip = (page - 1) * limit

        lab_orders = await self.db.lab_orders.find(

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

                for item in lab_orders

            ],

            "total": total

        }

    # ==========================================
    # Update
    # ==========================================

    async def update_lab_order(

        self,

        hospital_id: str,

        lab_order_id: str,

        update_data: dict

    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        safe_update = jsonable_encoder(
            update_data
        )

        return await self.db.lab_orders.update_one(

            {

                "hospital_id": hospital_id,

                "lab_order_id": lab_order_id

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

        lab_order_id: str,

        status: LabOrderStatus

    ):

        return await self.db.lab_orders.update_one(

            {

                "hospital_id": hospital_id,

                "lab_order_id": lab_order_id

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
    # Upload Report
    # ==========================================

    async def upload_report(

        self,

        hospital_id: str,

        lab_order_id: str,

        report_file: str

    ):

        return await self.db.lab_orders.update_one(

            {

                "hospital_id": hospital_id,

                "lab_order_id": lab_order_id

            },

            {

                "$set": {

                    "report_file": report_file,

                    "status": LabOrderStatus.REPORT_UPLOADED.value,

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }

            }

        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete_lab_order(

        self,

        hospital_id: str,

        lab_order_id: str

    ):

        return await self.db.lab_orders.delete_one(

            {

                "hospital_id": hospital_id,

                "lab_order_id": lab_order_id

            }

        )