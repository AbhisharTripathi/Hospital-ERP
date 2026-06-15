from fastapi import HTTPException,status
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest,TokenResponse
from app.core.security import (
    verify_password,
    create_access_token
)

class AuthService:
    def __init__(
            self,
            user_repository:UserRepository
    ):
        self.user_repo = user_repository
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