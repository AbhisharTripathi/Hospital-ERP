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
from app.repositories.doctor_schedule import (
    DoctorScheduleRepository
)

from app.services.doctor_schedule import (
    DoctorScheduleService
)
from app.repositories.appointment import AppointmentRepository
from app.services.appointment import AppointmentService
from app.repositories.dashboard import DashboardRepository

from app.services.dashboard import DashboardService
from app.repositories.billing import BillingRepository
from app.services.billing import BillingService
from app.repositories.prescription import (
    PrescriptionRepository
)

from app.services.prescription import (
    PrescriptionService
)
from app.repositories.vitals import VitalRepository

from app.services.vitals import VitalService


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

def get_doctor_schedule_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> DoctorScheduleRepository:

    return DoctorScheduleRepository(db)

def get_hospital_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> HospitalRepository:

    return HospitalRepository(db)
def get_department_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> DepartmentRepository:

    return DepartmentRepository(db)

def get_dashboard_repository(
    db: AsyncIOMotorDatabase = Depends(
        get_db
    )
) -> DashboardRepository:

    return DashboardRepository(db)
def get_appointment_repository(
    db=Depends(get_db)
):
    return AppointmentRepository(db)

def get_vital_repository(
    db=Depends(get_db)
):

    return VitalRepository(
        db
    )

def get_billing_repository(
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> BillingRepository:

    return BillingRepository(db)

# ===========================
# Prescription Repository
# ===========================

def get_prescription_repository(

    db=Depends(get_db)

):

    return PrescriptionRepository(db)


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

    department_repo: DepartmentRepository = Depends(
        get_department_repository
    ),

    counter_repo: CountersRepository = Depends(
        get_counters_repository
    ),

    email_service: EmailService = Depends(
        get_email_service
    )

):

    return DoctorService(

        doctor_repository=doctor_repo,

        user_repository=user_repo,

        department_repository=department_repo,

        counter_repository=counter_repo,

        email_service=email_service
    )

def get_doctor_schedule_service(

    schedule_repo: DoctorScheduleRepository = Depends(
        get_doctor_schedule_repository
    ),

    doctor_repo: DoctorRepository = Depends(
        get_doctor_repository
    ),

    counter_repo: CountersRepository = Depends(
        get_counters_repository
    )

) -> DoctorScheduleService:

    return DoctorScheduleService(

        schedule_repository=schedule_repo,

        doctor_repository=doctor_repo,

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


def get_dashboard_service(

    dashboard_repository: DashboardRepository = Depends(
        get_dashboard_repository
    )

) -> DashboardService:

    return DashboardService(

        dashboard_repository=dashboard_repository

    )

# ===========================
# Appointment Service
# ===========================




def get_appointment_service(

    appointment_repository: AppointmentRepository = Depends(
        get_appointment_repository
    ),

    patient_repository: PatientRepository = Depends(
        get_patient_repository
    ),

    doctor_repository: DoctorRepository = Depends(
        get_doctor_repository
    ),

    doctor_schedule_repository: DoctorScheduleRepository = Depends(
        get_doctor_schedule_repository
    ),

    counter_repository: CountersRepository = Depends(
        get_counters_repository
    )

):

    return AppointmentService(

        appointment_repository=appointment_repository,

        patient_repository=patient_repository,

        doctor_repository=doctor_repository,

        schedule_repository=doctor_schedule_repository,

        counter_repository=counter_repository

    )

def get_vital_service(

    vital_repository: VitalRepository = Depends(
        get_vital_repository
    ),

    appointment_repository: AppointmentRepository = Depends(
        get_appointment_repository
    ),

    patient_repository: PatientRepository = Depends(
        get_patient_repository
    ),

    doctor_repository: DoctorRepository = Depends(
        get_doctor_repository
    ),

    counter_repository: CountersRepository = Depends(
        get_counters_repository
    )

):

    return VitalService(

        vital_repository=vital_repository,

        appointment_repository=appointment_repository,

        patient_repository=patient_repository,

        doctor_repository=doctor_repository,

        counter_repository=counter_repository

    )
def get_billing_service(

    billing_repository: BillingRepository = Depends(
        get_billing_repository
    ),

    patient_repository: PatientRepository = Depends(
        get_patient_repository
    ),

    doctor_repository: DoctorRepository = Depends(
        get_doctor_repository
    ),

    appointment_repository: AppointmentRepository = Depends(
        get_appointment_repository
    ),

    counter_repository: CountersRepository = Depends(
        get_counters_repository
    )

) -> BillingService:

    return BillingService(

        billing_repository=billing_repository,

        patient_repository=patient_repository,

        doctor_repository=doctor_repository,

        appointment_repository=appointment_repository,

        counter_repository=counter_repository

    )

# ===========================
# Prescription Service
# ===========================

def get_prescription_service(

    prescription_repository: PrescriptionRepository = Depends(
        get_prescription_repository
    ),

    appointment_repository: AppointmentRepository = Depends(
        get_appointment_repository
    ),

    patient_repository: PatientRepository = Depends(
        get_patient_repository
    ),

    doctor_repository: DoctorRepository = Depends(
        get_doctor_repository
    ),

    counter_repository: CountersRepository = Depends(
        get_counters_repository
    )

):

    return PrescriptionService(

        prescription_repository=prescription_repository,

        appointment_repository=appointment_repository,

        patient_repository=patient_repository,

        doctor_repository=doctor_repository,

        counter_repository=counter_repository

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






