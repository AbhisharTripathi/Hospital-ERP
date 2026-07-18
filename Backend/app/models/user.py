from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

# pydantic = ODM (object development mapper)
class UserRole(str, Enum):
    # Management
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    HR = "HR"

    # Clinical
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    LAB_TECHNICIAN = "LAB_TECHNICIAN"
    PHARMACIST = "PHARMACIST"
    RADIOLOGIST = "RADIOLOGIST"

    # Front Office
    RECEPTIONIST = "RECEPTIONIST"
    CASHIER = "CASHIER"

    # Operations
    ACCOUNTANT = "ACCOUNTANT"
    STORE_MANAGER = "STORE_MANAGER"
    HOUSEKEEPING = "HOUSEKEEPING"
    SECURITY = "SECURITY"

    # External
    PATIENT = "PATIENT"
    

class UserStatus(str, Enum):
    INVITED = "INVITED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class UserName(BaseModel):
    first: str
    last: str | None = None


class UserContact(BaseModel):
    phone: str | None = None
    address: str | None = None


class UserModel(BaseModel):

    user_id: str

    hospital_id: str | None = None

    name: UserName | None = None

    username: str | None = None   # user id

    email: EmailStr

    password: str| None=None
    is_password_set: bool = False

    invite_token: str | None = None
    invite_token_expiry: datetime | None = None #for verifying email link

    role: UserRole

    permissions: list[str] = Field(default_factory=list) 

    department_id: str | None = None

    department: str | None = None

    

    contact: UserContact | None = None 

    metadata: dict[str, Any] = Field(default_factory=dict)

    status: UserStatus = UserStatus.ACTIVE
    is_active: bool = True

    created_by: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

