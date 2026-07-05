from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

# pydantic = ODM (object development mapper)
class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    RECEPTIONIST = "RECEPTIONIST"
    PHARMACIST = "PHARMACIST"
    LAB_TECHNICIAN = "LAB_TECHNICIAN"
    ACCOUNTANT = "ACCOUNTANT"
    PATIENT = "PATIENT"


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

    password: str

    role: UserRole

    permissions: list[str] = Field(default_factory=list) 

    department_id: str | None = None

    department: str | None = None

    employee_code: str | None = None

    contact: UserContact | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    is_active: bool = True

    created_by: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

