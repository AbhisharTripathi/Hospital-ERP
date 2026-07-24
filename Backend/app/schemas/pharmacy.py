from datetime import datetime

from pydantic import BaseModel, Field

from app.models.pharmacy import (
    PharmacyMedicine,
    PharmacyStatus
)


# ==========================================
# Create
# ==========================================

class PharmacyCreate(BaseModel):

    prescription_id: str


# ==========================================
# Update Medicine
# ==========================================

class PharmacyMedicineUpdate(BaseModel):

    medicine_name: str

    dispensed_quantity: int = Field(
        ge=0
    )

    remarks: str | None = Field(
        default=None,
        max_length=500
    )


# ==========================================
# Update
# ==========================================

class PharmacyUpdate(BaseModel):

    medicines: list[PharmacyMedicineUpdate]


# ==========================================
# Status Update
# ==========================================

class PharmacyStatusUpdate(BaseModel):

    status: PharmacyStatus


# ==========================================
# Response
# ==========================================

class PharmacyResponse(BaseModel):

    pharmacy_id: str

    hospital_id: str

    prescription_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    pharmacist_id: str | None

    medicines: list[PharmacyMedicine]

    status: PharmacyStatus

    dispensed_at: datetime | None

    created_at: datetime

    updated_at: datetime