from datetime import date, datetime, time

from pydantic import BaseModel, Field

from app.models.appointment import (
    AppointmentStatus,
    AppointmentType
)


class AppointmentCreate(BaseModel):

    patient_id: str

    doctor_id: str

    department_id: str

    appointment_date: date

    appointment_time: time

    appointment_type: AppointmentType = AppointmentType.NEW

    reason: str | None = Field(
        default=None,
        max_length=500
    )

    notes: str | None = Field(
        default=None,
        max_length=1000
    )


class AppointmentUpdate(BaseModel):

    appointment_date: date | None = None

    appointment_time: time | None = None

    appointment_type: AppointmentType | None = None

    reason: str | None = Field(
        default=None,
        max_length=500
    )

    notes: str | None = Field(
        default=None,
        max_length=1000
    )


class AppointmentStatusUpdate(BaseModel):

    status: AppointmentStatus


class AppointmentResponse(BaseModel):

    appointment_id: str

    hospital_id: str

    patient_id: str

    doctor_id: str

    department_id: str

    schedule_id: str

    appointment_date: date

    appointment_time: time

    token_number: int

    appointment_type: AppointmentType

    status: AppointmentStatus

    reason: str | None

    notes: str | None

    created_at: datetime

    updated_at: datetime