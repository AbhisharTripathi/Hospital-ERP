from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.prescription import (
    PrescriptionStatus,
    PrescriptionMedicine,
)


# ===========================================
# Create
# ===========================================

class PrescriptionCreate(BaseModel):

    appointment_id: str

    patient_id: str

    doctor_id: str

    diagnosis: str = Field(
        min_length=3,
        max_length=1000
    )

    advice: str | None = Field(
        default=None,
        max_length=1000
    )

    follow_up_date: date | None = None

    medicines: list[PrescriptionMedicine]


# ===========================================
# Update
# ===========================================

class PrescriptionUpdate(BaseModel):

    diagnosis: str | None = Field(
        default=None,
        min_length=3,
        max_length=1000
    )

    advice: str | None = Field(
        default=None,
        max_length=1000
    )

    follow_up_date: date | None = None

    medicines: list[PrescriptionMedicine] | None = None


# ===========================================
# Status Update
# ===========================================

class PrescriptionStatusUpdate(BaseModel):

    status: PrescriptionStatus


# ===========================================
# Response
# ===========================================

class PrescriptionResponse(BaseModel):

    prescription_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    diagnosis: str

    advice: str | None

    follow_up_date: date | None

    medicines: list[PrescriptionMedicine]

    status: PrescriptionStatus

    created_at: datetime

    updated_at: datetime