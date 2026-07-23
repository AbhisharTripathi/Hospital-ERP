from datetime import date, datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class PrescriptionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class MedicineTiming(str, Enum):
    BEFORE_FOOD = "BEFORE_FOOD"
    AFTER_FOOD = "AFTER_FOOD"
    WITH_FOOD = "WITH_FOOD"


class MedicineFrequency(str, Enum):
    ONCE_DAILY = "ONCE_DAILY"
    TWICE_DAILY = "TWICE_DAILY"
    THRICE_DAILY = "THRICE_DAILY"
    FOUR_TIMES_DAILY = "FOUR_TIMES_DAILY"
    SOS = "SOS"


class PrescriptionMedicine(BaseModel):

    medicine_name: str

    dosage: str

    frequency: MedicineFrequency

    duration: str

    timing: MedicineTiming

    instructions: str | None = None


class PrescriptionModel(BaseModel):

    prescription_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    diagnosis: str

    advice: str | None = None

    follow_up_date: date | None = None

    medicines: list[PrescriptionMedicine]

    status: PrescriptionStatus = PrescriptionStatus.ACTIVE

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )