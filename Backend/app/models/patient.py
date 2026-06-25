from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone, date
from typing import Optional
from enum import Enum

class BloodGroup(str,Enum):
    A_POSITIVE="A+"
    A_NEGATIVE="A-"
    AB_POSITIVE="AB+"
    AB_NEGATIVE="AB-"
    B_POSITIVE="B+"
    B_NEGATIVE="B-"
    O_POSITIVE="O+"
    O_NEGATIVE="O-"
    


    

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

    gender: Gender
    dob: date
   # password : str

    

    phone: str
    email: Optional[EmailStr] = None

    blood_group: Optional[BloodGroup] = None
    

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