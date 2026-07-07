from fastapi import Request,HTTPException, status,Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.counters import CountersRepository
from app.repositories.patient import PatientRepository
from app.repositories.user import UserRepository
from app.services.hospital import HospitalService
from app.services.patient import PatientServices
from app.services.auth import AuthService
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.core.security import decode_token
from app.models.user import UserRole
from app.repositories.doctor import DoctorRepository

from app.services.doctor import DoctorService
from app.repositories.hospital import HospitalRepository
from app.services.email import EmailService
from app.services.user import UserService


security = HTTPBearer()

def get_db(
    request: Request
) -> AsyncIOMotorDatabase:

    return request.app.state.db




def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> UserRepository:

    return UserRepository(db)


def get_patient_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> PatientRepository:

    return PatientRepository(db)


def get_counters_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> CountersRepository:

    return CountersRepository(db)

def get_doctor_repository(
    db: AsyncIOMotorDatabase = Depends(
        get_db
    )
):
    return DoctorRepository(db)

def get_hospital_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> HospitalRepository:

    return HospitalRepository(db)





def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    counter_repo: CountersRepository = Depends(get_counters_repository) # <-- Isko yahan upar arguments mein daal diya
) -> AuthService:
    
    return AuthService(
        user_repository=user_repo,
        counter_repository=counter_repo
    )

def get_email_service() -> EmailService:
    return EmailService()

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

def get_doctor_service(
    doctor_repo: DoctorRepository = Depends(
        get_doctor_repository
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
    counter_repo: CountersRepository = Depends(
        get_counters_repository
    ),
    
):
    return DoctorService(
        doctor_repository=doctor_repo,
        user_repository=user_repo,
        counter_repository=counter_repo,
        
    )

def get_hospital_service(
    hospital_repo: HospitalRepository = Depends(
        get_hospital_repository
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
    counter_repo: CountersRepository = Depends(
        get_counters_repository
    ),
    email_service: EmailService = Depends(
        get_email_service
    )
):
    return HospitalService(
        hospital_repository=hospital_repo,
        user_repository=user_repo,
        counter_repository=counter_repo,
        email_service=email_service
    )

def get_user_service(
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
    counter_repo: CountersRepository = Depends(
        get_counters_repository
    ),
    email_service: EmailService = Depends(
        get_email_service
    )
) -> UserService:

    return UserService(
        user_repository=user_repo,
        counter_repository=counter_repo,
        email_service=email_service
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


def require_role(
    *allowed_roles: UserRole
):

    async def role_checker(
        current_user = Depends(
            get_current_user
        )
    ):

        user_role = current_user.get(
            "role"
        )

        if user_role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )

        return current_user

    return role_checker



