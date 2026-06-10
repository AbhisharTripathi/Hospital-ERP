from pydantic import BaseModel,Field 
from datetime import datetime ,timezone
from typing import Optional

class Patient(BaseModel):
    patient_id: str
    first_name: str
    last_name: Optional[str] = None

    gender: str
    age: int

    mobile_number: str
    blood_group: Optional[str] = None
    address: Optional[str] = None

    emergency_contact_name: Optional[str] = None
    status: str = "ACTIVE"

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))