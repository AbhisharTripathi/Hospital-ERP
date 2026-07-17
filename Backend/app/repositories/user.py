from app.models.user import UserStatus
from datetime import datetime, timezone
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
    async def get_by_invite_token(
        self,
        token: str
    ):

        return await self.db.users.find_one(
            {
                "invite_token": token
            }
        )
    
    async def update_password(
        self,
        user_id: str,
        hashed_password: str
    ):

        return await self.db.users.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    "password": hashed_password,
                    "is_password_set": True,
                    "invite_token": None,
                    "invite_token_expiry": None,
                    "status": UserStatus.ACTIVE,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )  

    async def update_invite_token(
        self,
        user_id: str,
        token: str,
        expiry:datetime
        
    ):

        return await self.db.users.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    "invite_token": token,
                    "invite_token_expiry": expiry
                }
            }
        )  
    

    async def get_all_by_hospital(
        self,
        hospital_id: str
    ):

        cursor = self.db.users.find(
            {
                "hospital_id": hospital_id
            }
        )

        return await cursor.to_list(length=None)
    
    async def get_by_user_id_and_hospital(
        self,
        user_id: str,
        hospital_id: str
    ):

        return await self.db.users.find_one(
            {
                "user_id": user_id,
                "hospital_id": hospital_id
            }
        )
    
    async def update_employee(
        self,
        user_id: str,
        update_data: dict
    ):

        return await self.db.users.update_one(
            {
                "user_id": user_id
            },
            {
                "$set": update_data
            }
        )
    
    async def update_status(
        self,
        user_id: str,
        hospital_id: str,
        status: UserStatus
    ):

        return await self.db.users.update_one(
            {
                "user_id": user_id,
                "hospital_id": hospital_id
            },
            {
                "$set": {
                    "status": status.value,
                    "is_active": status == UserStatus.ACTIVE,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )