from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime
from app.models.patient import Gender

from app.models.doctor import DoctorStatus

class DoctorCreate(BaseModel):

    first_name: str= Field(
        min_length=2,
        max_length=55
    )
    last_name: Optional[str] = None

    email: EmailStr
    phone: str = Field(
        min_length=4,
        max_length=15
    )

    gender: Gender

    specialization: str

    qualification: str

    experience_years: int = 0

    consultation_fee: float = 0

    password: str

class DoctorUpdate(BaseModel):

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    phone: Optional[str] = None

    specialization: Optional[str] = None

    qualification: Optional[str] = None

    experience_years: Optional[int] = None

    consultation_fee: Optional[float] = None

class DoctorResponse(BaseModel):

    doctor_id: str

    user_id: str

    first_name: str
    last_name: Optional[str]

    email: EmailStr
    phone: str

    gender: str

    specialization: str

    qualification: str

    experience_years: int

    consultation_fee: float

    status: DoctorStatus

    created_at: datetime
    updated_at: datetime