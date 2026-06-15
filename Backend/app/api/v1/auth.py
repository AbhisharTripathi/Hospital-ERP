from fastapi import APIRouter,Depends
from app.dependencies import get_current_user

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth import AuthService
from app.dependencies import get_auth_service

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]

)

@router.post(
    "/login",
    response_model=TokenResponse
)

async def login(
    login_data:LoginRequest,
    auth_service:AuthService= Depends(
        get_auth_service
    )
):
    return await auth_service.login(
        login_data
    )
@router.get("/me")
async def get_me(
    current_user = Depends(
        get_current_user
    )
):

    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"]
    }