from datetime import datetime, timezone,date

from app.models.appointment import AppointmentStatus


class AppointmentRepository:

    def __init__(self, db):
        self.db = db

    # ---------------- Create ---------------- #

    async def create_appointment(
        self,
        appointment_data: dict
    ):
        result = await self.db.appointments.insert_one(
            appointment_data
        )
        return result.inserted_id

    # ---------------- Get By Appointment ID ---------------- #

    async def get_by_appointment_id(
        self,
        hospital_id: str,
        appointment_id: str
    ):
        return await self.db.appointments.find_one(
            {
                "hospital_id": hospital_id,
                "appointment_id": appointment_id
            }
        )

    # ---------------- Slot Already Booked ---------------- #

    async def get_by_slot(
        self,
        hospital_id: str,
        doctor_id: str,
        appointment_date: str|date,
        appointment_time: str
    ):  
        if isinstance(appointment_date, (date, datetime)):
            formatted_date = appointment_date.strftime("%Y-%m-%d")
        else:
            formatted_date = str(appointment_date)
        return await self.db.appointments.find_one(
            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "appointment_date": formatted_date,  # Direct string ("2026-07-25")
                "appointment_time": str(appointment_time),  # Direct string ("09:00:00")
                "status": {
                    "$ne": AppointmentStatus.CANCELLED.value
                }
            }
        )

    # ---------------- Token Number ---------------- #

    async def get_last_token(
        self,
        hospital_id: str,
        doctor_id: str,
        appointment_date: str
    ):

        return await self.db.appointments.find_one(

            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "appointment_date": appointment_date
            },

            sort=[("token_number", -1)]

        )
    async def get_appointments_by_day(
        self,
        hospital_id: str,
        doctor_id: str,
        appointment_date: date
    ):
        if hasattr(appointment_date, "strftime"):
            formatted_date = appointment_date.strftime("%Y-%m-%d")
        else:
            formatted_date = str(appointment_date)
        cursor = self.db.appointments.find(

            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "appointment_date": formatted_date,
                "status": {
                    "$nin": [
                        "CANCELLED",
                        "NO_SHOW"
                    ]
                }
            }

        ).sort(
            "token_number",
            1
        )

        return await cursor.to_list(length=None)

    # ---------------- Get All ---------------- #

    async def get_all_appointments(

        self,

        hospital_id: str,

        page: int = 1,

        limit: int = 20,

        search: str | None = None,

        doctor_id: str | None = None,

        patient_id: str | None = None,

        status: AppointmentStatus | None = None,

        appointment_date: str | None = None,

        sort_by: str = "appointment_date",

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

        if appointment_date:
            query["appointment_date"] = appointment_date

        if search:

            query["$or"] = [

                {
                    "appointment_id": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "patient_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "doctor_name": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.appointments.count_documents(
            query
        )

        skip = (page - 1) * limit

        appointments = await self.db.appointments.find(
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

            "items": appointments,

            "total": total

        }

    # ---------------- Update ---------------- #

    async def update_appointment(
        self,
        hospital_id: str,
        appointment_id: str,
        update_data: dict
    ):
        # 1. updated_at field set karein
        update_data["updated_at"] = datetime.now(timezone.utc)

        # 2. PyMongo serialization fix: date/datetime objects ko String me convert karein
        cleaned_data = {}
        for key, value in update_data.items():
            if isinstance(value, date) and not isinstance(value, datetime):
                # Pure date (e.g. 2026-07-22) -> "2026-07-22"
                cleaned_data[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, datetime):
                # Datetime -> ISO String format
                cleaned_data[key] = value.isoformat()
            else:
                cleaned_data[key] = value

        # 3. Cleaned dictionary ko database me update karein
        return await self.db.appointments.update_one(
            {
                "hospital_id": hospital_id,
                "appointment_id": appointment_id
            },
            {
                "$set": cleaned_data
            }
        )

    # ---------------- Update Status ---------------- #

    async def update_status(

        self,

        hospital_id: str,

        appointment_id: str,

        status: AppointmentStatus

    ):

        return await self.db.appointments.update_one(

            {

                "hospital_id": hospital_id,

                "appointment_id": appointment_id

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

    # ---------------- Delete ---------------- #

    async def delete_appointment(

        self,

        hospital_id: str,

        appointment_id: str

    ):

        return await self.db.appointments.delete_one(

            {

                "hospital_id": hospital_id,

                "appointment_id": appointment_id

            }

        )