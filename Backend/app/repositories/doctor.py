class DoctorRepository:

    def __init__(self, db):
        self.db = db

    async def create_doctor(
        self,
        doctor_data
    ):
        result = await self.db.doctors.insert_one(
            doctor_data
        )

        return result.inserted_id

    async def get_all_doctors(
        self,
        limit=100
    ):
        return await self.db.doctors.find().to_list(
            limit
        )

    async def get_doctor_by_id(
        self,
        doctor_id: str
    ):
        return await self.db.doctors.find_one(
            {
                "doctor_id": doctor_id
            }
        )

    async def get_by_user_id(
        self,
        user_id: str
    ):
        return await self.db.doctors.find_one(
            {
                "user_id": user_id
            }
        )

    async def update_by_doctor_id(
        self,
        doctor_id: str,
        update_data: dict
    ):
        return await self.db.doctors.update_one(
            {
                "doctor_id": doctor_id
            },
            {
                "$set": update_data
            }
        )