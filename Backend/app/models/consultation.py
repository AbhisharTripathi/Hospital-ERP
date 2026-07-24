from datetime import (
    date,
    datetime,
    timezone
)

from enum import Enum

from pydantic import (
    BaseModel,
    Field
)


# ==========================================
# Consultation Status
# ==========================================

class ConsultationStatus(str, Enum):

    IN_PROGRESS = "IN_PROGRESS"

    COMPLETED = "COMPLETED"

    CANCELLED = "CANCELLED"


# ==========================================
# Consultation Model
# ==========================================

class ConsultationModel(BaseModel):

    consultation_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    chief_complaint: str

    history_of_present_illness: str | None = None

    physical_examination: str | None = None

    diagnosis: str

    clinical_notes: str | None = None

    advice: str | None = None

    follow_up_date: date | None = None

    status: ConsultationStatus = ConsultationStatus.IN_PROGRESS

    created_by: str

    created_at: datetime = Field(

        default_factory=lambda: datetime.now(
            timezone.utc
        )

    )

    updated_at: datetime = Field(

        default_factory=lambda: datetime.now(
            timezone.utc
        )

    )