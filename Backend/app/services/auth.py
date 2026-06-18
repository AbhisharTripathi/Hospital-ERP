from fastapi import HTTPException,status
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest,TokenResponse
from app.core.security import (
    verify_password,
    create_access_token
)
from app.schemas.user import UserCreate
from app.models.user import UserModel
from app.core.security import hash_password
from app.utils.id_generator import IDGenerator


class AuthService:
    def __init__(
            self,
            user_repository:UserRepository,
            counter_repository
    ):
        self.user_repo = user_repository
        self.counter_repo=counter_repository
    async def login(
            self,
            login_data:LoginRequest
    )-> TokenResponse:
        
        user =await self.user_repo.get_by_email(
            login_data.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not user.get("is_active" ,True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        is_valid = verify_password(
            login_data.password,
            user["password"]
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        acess_token= create_access_token(
            {
                "user_id":user["user_id"],
                "role":user["role"]
            }
        )

        return TokenResponse(
            access_token=acess_token
        )



    async def register(
        self,
        user: UserCreate
    ):

        existing_user = await self.user_repo.get_by_email(
            user.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user_data = user.model_dump()

        user_data["password"] = hash_password(
            user.password
        )

        user_id = await IDGenerator.generate_user_id(
            self.counter_repo
        )

        user_data["user_id"]=user_id
        user_model=UserModel(
            **user_data
        )

        inserted_id = await self.user_repo.create_user(
            user_model.model_dump()
        )

        return{
            "user_id":user_id,
            "inserted_id": str(inserted_id)
        }
