from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole,UserStatus
from typing import Any


class EmployeeCreate(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: str | None = None

    email: EmailStr

    phone: str | None = None

    role: UserRole

    department_id: str | None = None

    department: str | None = None

    

    address: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmployeeResponse(BaseModel):

    user_id: str

    hospital_id: str

    first_name: str

    last_name: str | None

    email: EmailStr

    phone: str | None

    role: UserRole

    department: str | None

    status: UserStatus

    is_active: bool



class EmployeeUpdate(BaseModel):

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    last_name: str | None = None

    phone: str | None = None

    address: str | None = None

    role: UserRole | None = None

    department_id: str | None = None

    department: str | None = None

    

    metadata: dict = Field(
        default_factory=dict
)


