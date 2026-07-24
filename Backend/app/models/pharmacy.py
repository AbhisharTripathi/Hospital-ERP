from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Pharmacy Status
# ==========================================

class PharmacyStatus(str, Enum):

    PENDING = "PENDING"

    PARTIALLY_DISPENSED = "PARTIALLY_DISPENSED"

    DISPENSED = "DISPENSED"

    CANCELLED = "CANCELLED"


# ==========================================
# Medicine Item
# ==========================================

class PharmacyMedicine(BaseModel):

    medicine_name: str

    dosage: str

    frequency: str

    duration: str

    timing: str

    prescribed_quantity: int = Field(
        gt=0
    )

    dispensed_quantity: int = Field(
        default=0,
        ge=0
    )

    remarks: str | None = None


# ==========================================
# Pharmacy Model
# ==========================================

class PharmacyModel(BaseModel):

    pharmacy_id: str

    hospital_id: str

    prescription_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str
    
    pharmacist_id: str | None = None

    medicines: list[PharmacyMedicine]

    status: PharmacyStatus = PharmacyStatus.PENDING

    dispensed_at: datetime | None = None

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )