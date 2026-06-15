from fastapi import Request, Depends,HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.counters import CountersRepository
from app.repositories.patient import PatientRepository
from app.repositories.user import UserRepository

from app.services.patient import PatientServices
from app.services.auth import AuthService
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.core.security import decode_token

security = HTTPBearer()

def get_db(
    request: Request
) -> AsyncIOMotorDatabase:

    return request.app.state.db


def get_counters_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> CountersRepository:

    return CountersRepository(db)


def get_patient_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> PatientRepository:

    return PatientRepository(db)


def get_patient_services(
    patient_repository: PatientRepository = Depends(
        get_patient_repository
    ),
    counter_repository: CountersRepository = Depends(
        get_counters_repository
    )
) -> PatientServices:

    return PatientServices(
        patient_repository,
        counter_repository
    )


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> UserRepository:

    return UserRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(
        get_user_repository
    )
) -> AuthService:

    return AuthService(
        user_repository=user_repo
    )
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    )
):

    token = credentials.credentials

    try:

        payload = decode_token(token)

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = await user_repo.get_by_user_id(
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )