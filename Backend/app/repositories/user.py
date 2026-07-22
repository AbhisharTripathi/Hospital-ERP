from datetime import datetime, timezone

from app.models.user import UserStatus


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
        expiry: datetime
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
        hospital_id: str,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        role=None,
        status=None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ):

        query = {
            "hospital_id": hospital_id
        }

        if role:
            query["role"] = role

        if status:
            query["status"] = status

        if search:
            query["$or"] = [

                {
                    "name.first": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "name.last": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "email": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "contact.phone": {
                        "$regex": search,
                        "$options": "i"
                    }
                },

                {
                    "department": {
                        "$regex": search,
                        "$options": "i"
                    }
                }

            ]

        total = await self.db.users.count_documents(query)

        skip = (page - 1) * limit

        users = await self.db.users.find(
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
            "items": users,
            "total": total
        }

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