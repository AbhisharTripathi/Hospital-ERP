from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone, date
from typing import Optional
from enum import Enum


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class PatientStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DECEASED = "DECEASED"


class PatientModel(BaseModel):
    patient_id: str

    first_name: str
    last_name: Optional[str] = None

    password : str

    gender: Gender
    dob: datetime

    phone: str
    email: Optional[EmailStr] = None

    blood_group: Optional[str] = None

    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    status: PatientStatus = PatientStatus.ACTIVE

    notes: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )