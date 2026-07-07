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
    EmployeeResponse,EmployeeUpdate
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
        print("===== Sending Invitation Email =====")
        await self.email_service.send_invitation_email(
            employee_name=user_model.name.first,
            email=user_model.email,
            invite_token=invite_token
        )
        print("===== Invitation Email Sent =====")
        
        
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
    
    
    
    async def get_all_employees(
        self,
        current_user:dict
    ):
        users = await self.user_repo.get_all_by_hospital(
        current_user["hospital_id"]
        )
        employees = []

        for user in users:

            employees.append(
                EmployeeResponse(
                    user_id=user["user_id"],
                    hospital_id=user["hospital_id"],
                    first_name=user["name"]["first"],
                    last_name=user["name"].get("last"),
                    email=user["email"],
                    phone=user.get("contact", {}).get("phone"),
                    role=user["role"],
                    department=user.get("department"),
                    status=user.get("status"),
                    is_active=user.get("is_active", True)
                )
            )

        return employees
    
    
    
    async def get_employee(
        self,
        current_user,
        user_id: str
    ):
        user = await self.user_repo.get_by_user_id_and_hospital(
            user_id,
            current_user["hospital_id"]
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )
    
        return EmployeeResponse(
            user_id=user["user_id"],
            hospital_id=user["hospital_id"],
            first_name=user["name"]["first"],
            last_name=user["name"].get("last"),
            email=user["email"],
            phone=user.get("contact", {}).get("phone"),
            role=user["role"],
            department=user.get("department"),
            status=user.get("status"),
            is_active=user.get("is_active", True)
        )
    
    
    
    async def update_employee(
        self,
        current_user,
        user_id: str,
        employee_data: EmployeeUpdate
    ):

        user = await self.user_repo.get_by_user_id_and_hospital(
            user_id=user_id,
            hospital_id=current_user["hospital_id"]
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        update_data = {}
        update_fields = employee_data.model_dump(
            exclude_unset=True
        )
        if "first_name" in update_fields:
            update_data["name.first"] = update_fields["first_name"]

        if "last_name" in update_fields:
            update_data["name.last"] = update_fields["last_name"]

        if "phone" in update_fields:
            update_data["contact.phone"] = update_fields["phone"]

        if "address" in update_fields:
            update_data["contact.address"] = update_fields["address"]

        if "department" in update_fields:
            update_data["department"] = update_fields["department"]

        if "department_id" in update_fields:
            update_data["department_id"] = update_fields["department_id"]

        if "metadata" in update_fields:
            update_data["metadata"] = update_fields["metadata"]
            

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        await self.user_repo.update_employee(
            user_id=user_id,
            update_data=update_data
        )

        updated_user = await self.user_repo.get_by_user_id_and_hospital(
            user_id=user_id,
            hospital_id=current_user["hospital_id"]
        )
        print(employee_data)
        print(employee_data.model_dump())
        print(employee_data.model_dump(exclude_unset=True))

        return EmployeeResponse(
            user_id=updated_user["user_id"],
            hospital_id=updated_user["hospital_id"],
            first_name=updated_user["name"]["first"],
            last_name=updated_user["name"].get("last"),
            email=updated_user["email"],
            phone=updated_user.get("contact", {}).get("phone"),
            role=updated_user["role"],
            department=updated_user.get("department"),
            status=updated_user["status"],
            is_active=updated_user["is_active"]
        )
    
    