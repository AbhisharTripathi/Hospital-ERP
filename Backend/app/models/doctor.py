from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from .patient import Gender

class DoctorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class DoctorModel(BaseModel):

    doctor_id: str

    user_id: str

    first_name: str
    last_name: Optional[str] = None

    email: EmailStr
    phone: str

    gender: Gender

    specialization: str

    qualification: str

    experience_years: int = 0

    consultation_fee: float = 0

    status: DoctorStatus = DoctorStatus.ACTIVE

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )