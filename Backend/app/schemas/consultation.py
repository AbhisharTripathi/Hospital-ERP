from datetime import (
    date,
    datetime
)

from pydantic import (
    BaseModel,
    Field
)

from app.models.consultation import (
    ConsultationStatus
)

# ==========================================
# Create
# ==========================================

class ConsultationCreate(BaseModel):

    appointment_id: str

    

    chief_complaint: str = Field(

        min_length=3,

        max_length=1000

    )

    history_of_present_illness: str | None = Field(

        default=None,

        max_length=3000

    )

    physical_examination: str | None = Field(

        default=None,

        max_length=3000

    )

    diagnosis: str = Field(

        min_length=3,

        max_length=2000

    )

    clinical_notes: str | None = Field(

        default=None,

        max_length=5000

    )

    advice: str | None = Field(

        default=None,

        max_length=3000

    )

    follow_up_date: date | None = None


# ==========================================
# Update
# ==========================================

class ConsultationUpdate(BaseModel):

    chief_complaint: str | None = Field(

        default=None,

        min_length=3,

        max_length=1000

    )

    history_of_present_illness: str | None = Field(

        default=None,

        max_length=3000

    )

    physical_examination: str | None = Field(

        default=None,

        max_length=3000

    )

    diagnosis: str | None = Field(

        default=None,

        min_length=3,

        max_length=2000

    )

    clinical_notes: str | None = Field(

        default=None,

        max_length=5000

    )

    advice: str | None = Field(

        default=None,

        max_length=3000

    )

    follow_up_date: date | None = None


# ==========================================
# Status Update
# ==========================================

class ConsultationStatusUpdate(BaseModel):

    status: ConsultationStatus


# ==========================================
# Response
# ==========================================

class ConsultationResponse(BaseModel):

    consultation_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    chief_complaint: str

    history_of_present_illness: str | None

    physical_examination: str | None

    diagnosis: str

    clinical_notes: str | None

    advice: str | None

    follow_up_date: date | None

    status: ConsultationStatus

    created_at: datetime

    updated_at: datetime