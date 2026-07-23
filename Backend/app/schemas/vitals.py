from datetime import (
    datetime
)

from pydantic import (
    BaseModel,
    Field
)

from app.models.vitals import (
    VitalStatus
)


# ==========================================
# Create
# ==========================================

class VitalCreate(BaseModel):

    appointment_id: str

    patient_id: str

    doctor_id: str

    height_cm: float | None = Field(
        default=None,
        ge=30,
        le=300
    )

    weight_kg: float | None = Field(
        default=None,
        ge=1,
        le=500
    )

    temperature_c: float | None = Field(
        default=None,
        ge=30,
        le=45
    )

    pulse_rate: int | None = Field(
        default=None,
        ge=20,
        le=250
    )

    respiratory_rate: int | None = Field(
        default=None,
        ge=5,
        le=80
    )

    systolic_bp: int | None = Field(
        default=None,
        ge=50,
        le=300
    )

    diastolic_bp: int | None = Field(
        default=None,
        ge=30,
        le=200
    )

    spo2: int | None = Field(
        default=None,
        ge=50,
        le=100
    )

    blood_sugar: float | None = Field(
        default=None,
        ge=20,
        le=1000
    )

    chief_complaint: str | None = Field(
        default=None,
        max_length=1000
    )

    remarks: str | None = Field(
        default=None,
        max_length=1000
    )


# ==========================================
# Update
# ==========================================

class VitalUpdate(BaseModel):

    height_cm: float | None = Field(
        default=None,
        ge=30,
        le=300
    )

    weight_kg: float | None = Field(
        default=None,
        ge=1,
        le=500
    )

    temperature_c: float | None = Field(
        default=None,
        ge=30,
        le=45
    )

    pulse_rate: int | None = Field(
        default=None,
        ge=20,
        le=250
    )

    respiratory_rate: int | None = Field(
        default=None,
        ge=5,
        le=80
    )

    systolic_bp: int | None = Field(
        default=None,
        ge=50,
        le=300
    )

    diastolic_bp: int | None = Field(
        default=None,
        ge=30,
        le=200
    )

    spo2: int | None = Field(
        default=None,
        ge=50,
        le=100
    )

    blood_sugar: float | None = Field(
        default=None,
        ge=20,
        le=1000
    )

    chief_complaint: str | None = Field(
        default=None,
        max_length=1000
    )

    remarks: str | None = Field(
        default=None,
        max_length=1000
    )


# ==========================================
# Status Update
# ==========================================

class VitalStatusUpdate(BaseModel):

    status: VitalStatus


# ==========================================
# Response
# ==========================================

class VitalResponse(BaseModel):

    vital_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    height_cm: float | None

    weight_kg: float | None

    bmi: float | None

    temperature_c: float | None

    pulse_rate: int | None

    respiratory_rate: int | None

    systolic_bp: int | None

    diastolic_bp: int | None

    spo2: int | None

    blood_sugar: float | None

    chief_complaint: str | None

    remarks: str | None

    status: VitalStatus

    recorded_by: str

    recorded_at: datetime

    updated_at: datetime
    