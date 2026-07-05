from fastapi import APIRouter, Depends, status

from app.dependencies import (
    get_auth_service,
    get_current_user,
    get_hospital_service,
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

from app.schemas.user import UserCreate

from app.schemas.hospital import (
    HospitalOwnerRegister,
    HospitalRegisterResponse,
)

from app.services.auth import AuthService
from app.services.hospital import HospitalService
from app.services.email import EmailService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(login_data)


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "role": current_user["role"],
    }


# Old endpoint (temporary)
@router.post("/register")
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(user)


@router.post(
    "/register-hospital",
    response_model=HospitalRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_hospital(
    register_data: HospitalOwnerRegister,
    hospital_service: HospitalService = Depends(
        get_hospital_service
    ),
):
    return await hospital_service.register_hospital_owner(
        register_data
    )

@router.get("/test-email")
async def test_email():

    email_service = EmailService()

    await email_service.send_email(
        subject="Hospital ERP SMTP Test",
        recipients=["akm22150809@gmail.com"],
        body="""
        <h2>Hospital ERP</h2>

        <h3>SMTP Working Successfully 🎉</h3>

        <p>Congratulations!</p>

        <p>Your FastAPI SMTP configuration is working.</p>
        """
    )

    return {
        "message": "Email Sent Successfully"
    }