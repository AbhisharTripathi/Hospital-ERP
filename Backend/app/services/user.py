from datetime import datetime, timedelta, timezone
import secrets  #ye crptographically secure hota hai isi ko email me bhejega pahle "random" use hota tha 

from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user import (
    UserModel,
    UserName,
    UserContact,
    UserStatus
)

from app.repositories.user import UserRepository
from app.repositories.counters import CountersRepository

from app.schemas.user import (
    EmployeeCreate,
    EmployeeResponse
)

from app.services.email import EmailService

from app.utils.id_generator import IDGenerator

class UserService:

    def __init__(
        self,
        user_repository: UserRepository,
        counter_repository: CountersRepository,
        email_service: EmailService
    ):

        self.user_repo = user_repository
        self.counter_repo = counter_repository
        self.email_service = email_service
   
    async def create_employee(
        self,
        current_user,
        employee_data: EmployeeCreate
    ):

        existing_user = await self.user_repo.get_by_email(
            employee_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

        user_id = await IDGenerator.generate_user_id(
            self.counter_repo
        )

        invite_token = secrets.token_urlsafe(32)

        invite_token_expiry = (
            datetime.now(timezone.utc)
            + timedelta(hours=24)
        )

        user_model = UserModel(
            user_id=user_id,

            hospital_id=current_user["hospital_id"],

            name=UserName(
                first=employee_data.first_name,
                last=employee_data.last_name
            ),

            username=employee_data.email.split("@")[0],

            email=employee_data.email,

            password=None,

            role=employee_data.role,

            contact=UserContact(
                phone=employee_data.phone,
                address=employee_data.address
            ),

            department_id=employee_data.department_id,

            department=employee_data.department,

            metadata=employee_data.metadata,

            is_password_set=False,

            invite_token=invite_token,

            invite_token_expiry=invite_token_expiry,

            status=UserStatus.INVITED,

            created_by=current_user["user_id"]
        )
        await self.user_repo.create_user(
            user_model.model_dump(mode="json")
        )
        await self.email_service.send_invitation_email(
            employee_name=user_model.name.first,
            email=user_model.email,
            invite_token=invite_token
        )
        
        
        
        return EmployeeResponse(
            user_id=user_model.user_id,
            hospital_id=user_model.hospital_id,
            first_name=user_model.name.first,
            last_name=user_model.name.last,
            email=user_model.email,
            phone=user_model.contact.phone if user_model.contact else None,
            role=user_model.role,
            department=user_model.department,
            status=user_model.status,
            is_active=user_model.is_active
        )