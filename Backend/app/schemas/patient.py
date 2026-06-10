from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import date

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class PatientCreate(BaseModel):
    first_name : str = Field(
        min_length=2,
        max_length = 50,
        description="First name must be between 2 to 50 characters long"
    )
    last_name : str | None = None
    password : str | None = None
    phone : str = Field(..., max_length = 15)
    email : EmailStr | None = None
    gender : Gender
    dob : date
    blood_group : str | None = None
    address : str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    notes : str | None = None
