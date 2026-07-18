from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime
from app.models.patient import Gender

from app.models.doctor import DoctorStatus


class DoctorCreate(BaseModel):

    user_id: str

    department_id: str

    license_number: str = Field(
        min_length=5,
        max_length=50
    )

    qualification: str

    specialization: str

    experience_years: int = 0

    consultation_fee: float = 0

class UpdateDoctorStatus(BaseModel):
    status: DoctorStatus   

class DoctorUpdate(BaseModel):

    department_id: str | None = None

    qualification: str | None = None

    specialization: str | None = None

    experience_years: int | None = None

    consultation_fee: float | None = None

    joining_date: datetime | None = None

class DoctorResponse(BaseModel):

    doctor_id: str

    user_id: str

    first_name: str
    last_name: Optional[str]

    email: EmailStr
    phone: str

    gender: str
    department_id: str
    specialization: str

    qualification: str

    experience_years: int

    consultation_fee: float

    status: DoctorStatus
    joining_date: datetime
     
    created_at: datetime
    updated_at: datetime