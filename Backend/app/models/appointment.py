from datetime import date, datetime, time, timezone
from enum import Enum

from pydantic import BaseModel, Field


class AppointmentStatus(str, Enum):
    BOOKED = "BOOKED"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class AppointmentType(str, Enum):
    NEW = "NEW"
    FOLLOW_UP = "FOLLOW_UP"
    EMERGENCY = "EMERGENCY"


class AppointmentModel(BaseModel):
    patient_name: str

    doctor_name: str
    appointment_id: str

    hospital_id: str

    patient_id: str

    doctor_id: str

    department_id: str

    schedule_id: str

    appointment_date: date

    appointment_time: time

    token_number: int

    appointment_type: AppointmentType = AppointmentType.NEW

    status: AppointmentStatus = AppointmentStatus.BOOKED

    reason: str | None = None

    notes: str | None = None

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )