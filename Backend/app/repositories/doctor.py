from datetime import datetime, timezone

from app.models.doctor import DoctorStatus


class DoctorRepository:

    def __init__(self, db):
        self.db = db

    # ---------------- Create ---------------- #

    async def create_doctor(
        self,
        doctor_data: dict
    ):

        result = await self.db.doctors.insert_one(
            doctor_data
        )

        return result.inserted_id

    # ---------------- Get All ---------------- #

    async def get_all_doctors(
        self,
        hospital_id: str,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        department_id: str | None = None,
        status: DoctorStatus | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):

        query = {
            "hospital_id": hospital_id
        }

        if department_id:
            query["department_id"] = department_id

        if status:
            query["status"] = status

        if search:

            query["$or"] = [

                {
                    "license_number": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "qualification": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "specialization": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.doctors.count_documents(
            query
        )

        skip = (page - 1) * limit

        doctors = await self.db.doctors.find(
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
            "items": doctors,
            "total": total
        }

    # ---------------- Get By ID ---------------- #

    async def get_doctor_by_id(
        self,
        doctor_id: str,
        hospital_id: str
    ):

        return await self.db.doctors.find_one(
            {
                "doctor_id": doctor_id,
                "hospital_id": hospital_id
            }
        )

    # ---------------- Get By User ---------------- #

    async def get_by_user_id(
        self,
        user_id: str,
        hospital_id: str
    ):

        return await self.db.doctors.find_one(
            {
                "user_id": user_id,
                "hospital_id": hospital_id
            }
        )

    # ---------------- Get By License ---------------- #

    async def get_by_license_number(
        self,
        hospital_id: str,
        license_number: str
    ):

        return await self.db.doctors.find_one(
            {
                "hospital_id": hospital_id,
                "license_number": license_number
            }
        )

    # ---------------- Department Doctors ---------------- #

    async def get_by_department(
        self,
        hospital_id: str,
        department_id: str
    ):

        return await self.db.doctors.find(
            {
                "hospital_id": hospital_id,
                "department_id": department_id,
                "status": DoctorStatus.ACTIVE
            }
        ).to_list(
            length=None
        )

    # ---------------- Update ---------------- #

    async def update_doctor(
        self,
        doctor_id: str,
        hospital_id: str,
        update_data: dict
    ):

        return await self.db.doctors.update_one(
            {
                "doctor_id": doctor_id,
                "hospital_id": hospital_id
            },
            {
                "$set": update_data
            }
        )
    async def get_active_doctor(
        self,
        hospital_id: str,
        doctor_id: str
    ):

        return await self.db.doctors.find_one(

            {
                "hospital_id": hospital_id,
                "doctor_id": doctor_id,
                "status": DoctorStatus.ACTIVE
            }

        )
    # ---------------- Status ---------------- #

    async def update_status(
        self,
        doctor_id: str,
        hospital_id: str,
        status: DoctorStatus
    ):

        return await self.db.doctors.update_one(

            {
                "doctor_id": doctor_id,
                "hospital_id": hospital_id
            },

            {
                "$set": {

                    "status": status,

                    "updated_at": datetime.now(
                        timezone.utc
                    )

                }
            }

        )