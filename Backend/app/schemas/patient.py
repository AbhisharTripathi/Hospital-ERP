from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=50
    )

    gender: str

    age: int = Field(
        gt=0,
        lt=150
    )

    mobile_number: str = Field(
        min_length=10,
        max_length=15
    )

    email: Optional[EmailStr] = None

    blood_group: Optional[str] = None

    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    last_name: Optional[str] = Field(
        default=None,
        max_length=50
    )

    gender: Optional[str] = None

    age: Optional[int] = Field(
        default=None,
        gt=0,
        lt=150
    )

    mobile_number: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    email: Optional[EmailStr] = None

    blood_group: Optional[str] = None

    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None

class PatientResponse(BaseModel):
    patient_id: str

    first_name: str

    last_name: Optional[str] = None

    gender: str

    age: int

    mobile_number: str

    email: Optional[str] = None

    blood_group: Optional[str] = None

    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None

    emergency_contact_number: Optional[str] = None

    status: str

    created_at: datetime

    updated_at: datetime