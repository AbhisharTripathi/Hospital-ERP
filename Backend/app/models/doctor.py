from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class DoctorStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Gender(str,Enum):
    MALE= "MALE"
    FEMALE="FEMALE"
    OTHER= "OTHER"



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
    gender: Gender

    status:DoctorStatus= DoctorStatus.ACTIVE

    availability: dict = Field(default_factory=dict)

    created_at: datetime=Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime=Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

# DoctorModel.model_rebuild()