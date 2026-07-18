from datetime import datetime, timezone

from app.models.doctor_schedule import DayOfWeek


class DoctorScheduleRepository:

    def __init__(self, db):
        self.db = db

    # ---------------- Create ---------------- #

    async def create_schedule(
        self,
        schedule_data: dict
    ):

        result = await self.db.doctor_schedules.insert_one(
            schedule_data
        )

        return result.inserted_id

    # ---------------- Get By Schedule ID ---------------- #

    async def get_by_schedule_id(
        self,
        schedule_id: str,
        hospital_id: str
    ):

        return await self.db.doctor_schedules.find_one(
            {
                "schedule_id": schedule_id,
                "hospital_id": hospital_id
            }
        )

    # ---------------- Get Doctor Schedules ---------------- #

    async def get_by_doctor(
        self,
        hospital_id: str,
        doctor_id: str
    ):

        cursor = self.db.doctor_schedules.find(
            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id
            }
        ).sort(
            "day_of_week",
            1
        )

        return await cursor.to_list(length=None)

    # ---------------- Get Day Schedule ---------------- #

    async def get_by_day(
        self,
        hospital_id: str,
        doctor_id: str,
        day_of_week: DayOfWeek
    ):

        cursor = self.db.doctor_schedules.find(
            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "day_of_week": day_of_week
            }
        )

        return await cursor.to_list(length=None)

    # ---------------- Overlap Check ---------------- #

    async def get_schedule_overlap(
        self,
        hospital_id: str,
        doctor_id: str,
        day_of_week: DayOfWeek
    ):

        cursor = self.db.doctor_schedules.find(
            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "day_of_week": day_of_week,
                "is_active": True
            }
        )

        return await cursor.to_list(length=None)

    # ---------------- get_schedule_id_except_current ---------------- #
    async def get_by_schedule_id_except_current(
        self,
        hospital_id: str,
        doctor_id: str,
        day_of_week,
        schedule_id: str
    ):

        cursor = self.db.doctor_schedules.find(

            {
                "hospital_id": hospital_id,

                "doctor_id": doctor_id,

                "day_of_week": day_of_week,

                "schedule_id": {
                    "$ne": schedule_id
                },

                "is_active": True
            }

        )

        return await cursor.to_list(length=None)
    
    # ---------------- Update ---------------- #

    async def update_schedule(
        self,
        schedule_id: str,
        hospital_id: str,
        update_data: dict
    ):

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        return await self.db.doctor_schedules.update_one(

            {
                "schedule_id": schedule_id,
                "hospital_id": hospital_id
            },

            {
                "$set": update_data
            }

        )

    # ---------------- Status ---------------- #

    async def update_status(
        self,
        schedule_id: str,
        hospital_id: str,
        is_active: bool
    ):

        return await self.db.doctor_schedules.update_one(

            {
                "schedule_id": schedule_id,
                "hospital_id": hospital_id
            },

            {
                "$set": {

                    "is_active": is_active,

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }
            }

        )

    # ---------------- Delete ---------------- #

    async def delete_schedule(
        self,
        schedule_id: str,
        hospital_id: str
    ):

        return await self.db.doctor_schedules.delete_one(
            {
                "schedule_id": schedule_id,
                "hospital_id": hospital_id
            }
        )