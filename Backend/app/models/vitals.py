from datetime import datetime, timezone
from enum import Enum

from pydantic import (
    BaseModel,
    Field
)


class VitalStatus(str, Enum):

    RECORDED = "RECORDED"

    VERIFIED = "VERIFIED"


class VitalModel(BaseModel):

    # ==========================================
    # IDs
    # ==========================================

    vital_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    # ==========================================
    # Physical Measurements
    # ==========================================

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

    bmi: float | None = None

    # ==========================================
    # Vital Signs
    # ==========================================

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

    # ==========================================
    # Clinical
    # ==========================================

    chief_complaint: str | None = Field(
        default=None,
        max_length=1000
    )

    remarks: str | None = Field(
        default=None,
        max_length=1000
    )

    status: VitalStatus = VitalStatus.RECORDED

    # ==========================================
    # Audit
    # ==========================================

    recorded_by: str

    recorded_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

