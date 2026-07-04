from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone

# pydantic = ODM (object development mapper)
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"
    PATIENT = "PATIENT"
    LAB_TECHNICIAN = "LAB_TECHNICIAN"
    PHARMACIST = "PHARMACIST"


class UserModel(BaseModel):

    user_id: str

    username: str

    email: EmailStr

    password: str

    role: UserRole

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

