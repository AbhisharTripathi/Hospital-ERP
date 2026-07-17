from fastapi import (
    Request,
    HTTPException,
    status,
    Depends
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import decode_token

from app.models.user import (
    UserRole,
    UserStatus
)

from app.repositories.user import UserRepository
from app.repositories.patient import PatientRepository
from app.repositories.counters import CountersRepository
from app.repositories.doctor import DoctorRepository
from app.repositories.hospital import HospitalRepository

from app.services.auth import AuthService
from app.services.patient import PatientServices
from app.services.doctor import DoctorService
from app.services.hospital import HospitalService
from app.services.user import UserService
from app.services.email import EmailService
from app.repositories.department import DepartmentRepository
from app.services.department import DepartmentService

security = HTTPBearer()


# ==========================
# Database
# ==========================

def get_db(
    request: Request
) -> AsyncIOMotorDatabase:

    return request.app.state.db


# ==========================
# Repositories
# ==========================

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
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> DoctorRepository:

    return DoctorRepository(db)


def get_hospital_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> HospitalRepository:

    return HospitalRepository(db)
def get_department_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> DepartmentRepository:

    return DepartmentRepository(db)

# ==========================
# Services
# ==========================

def get_email_service() -> EmailService:

    return EmailService()


def get_auth_service(
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
    counter_repo: CountersRepository = Depends(
        get_counters_repository
    )
) -> AuthService:

    return AuthService(
        user_repository=user_repo,
        counter_repository=counter_repo
    )


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
    )
) -> DoctorService:

    return DoctorService(
        doctor_repository=doctor_repo,
        user_repository=user_repo,
        counter_repository=counter_repo
    )

def get_department_service(
    department_repo: DepartmentRepository = Depends(
        get_department_repository
    ),
    counter_repo: CountersRepository = Depends(
        get_counters_repository
    )
) -> DepartmentService:

    return DepartmentService(
        department_repository=department_repo,
        counter_repository=counter_repo
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
    ),
    department_service: DepartmentService = Depends(
        get_department_service
    )
) -> HospitalService:

    return HospitalService(
        hospital_repository=hospital_repo,
        user_repository=user_repo,
        counter_repository=counter_repo,
        email_service=email_service,
        department_service=department_service
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




# ==========================
# Authentication
# ==========================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    )
):

    token = credentials.credentials

    # Token decode
    try:
        payload = decode_token(token)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

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


# ==========================
# Role Authorization
# ==========================

def require_role(
    *allowed_roles: UserRole
):

    async def role_checker(
        current_user: dict = Depends(
            get_current_user
        )
    ):

        if not current_user.get(
            "is_active",
            True
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        if current_user.get(
            "status"
        ) != UserStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not active"
            )

        if current_user.get(
            "role"
        ) not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )

        return current_user

    return role_checker