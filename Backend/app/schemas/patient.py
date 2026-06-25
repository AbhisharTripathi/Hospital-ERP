from pydantic import BaseModel, EmailStr, Field
from datetime import date,datetime
from typing import Optional

from app.models.patient import Gender,BloodGroup,PatientStatus

class PatientCreate(BaseModel):
    first_name : str = Field(
        min_length=2,
        max_length = 50,
        description="First name must be between 2 to 50 characters long"
    )
    last_name : str | None = None
    password : str | None = None # password baad me htna chahiye kyuki patient khud apna account nahi banayega
    phone : str = Field(..., max_length = 15)
    email :  Optional[EmailStr] = None
    gender : Gender
    dob : date
    blood_group : BloodGroup | None = None
    address : str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    notes : str | None = None




class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    gender: Optional[Gender] = None
    dob: Optional[date] = None

    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    blood_group: Optional[BloodGroup] = None

    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

    notes: Optional[str] = None



class PatientResponse(BaseModel):
    patient_id: str

    first_name: str
    last_name: Optional[str]

    gender: Gender
    dob: date

    phone: str
    email: Optional[EmailStr]

    blood_group: Optional[BloodGroup]

    address: Optional[str]

    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]

    status: PatientStatus

    notes: Optional[str]

    created_at: datetime
    updated_at: datetime


class PatientSearch(BaseModel):
    patient_id: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    address: Optional[str]=None

