class UserRepository:

    def __init__(self, db):
        self.db = db

    async def create_user(
        self,
        user_data: dict
    ):
        result = await self.db.users.insert_one(
            user_data
        )
        return result.inserted_id

    async def get_by_email(
        self,
        email: str,
        hospital_id: str | None = None
    ):
        query = {
            "email": email
        }

        if hospital_id is not None:
            query["hospital_id"] = hospital_id

        return await self.db.users.find_one(query)

    async def get_by_user_id(
        self,
        user_id: str
    ):
        return await self.db.users.find_one(
            {
                "user_id": user_id
            }
        )

    async def update_user(
        self,
        user_id: str,
        updated_data: dict
    ):
        return await self.db.users.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": updated_data
            }
        )