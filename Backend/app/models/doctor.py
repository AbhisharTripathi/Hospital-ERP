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

    hospital_id: str

    department_id: str

    license_number: str

    qualification: str

    specialization: str

    experience_years: int=0

    consultation_fee: float=0

    joining_date: datetime


    status: DoctorStatus.ACTIVE

    availability: dict = Field(default_factory=dict)

    created_at: datetime

    updated_at: datetime

  