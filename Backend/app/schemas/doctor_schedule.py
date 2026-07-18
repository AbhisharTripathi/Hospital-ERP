from datetime import datetime, time

from pydantic import BaseModel, Field

from app.models.doctor_schedule import DayOfWeek


class DoctorScheduleCreate(BaseModel):

    doctor_id: str

    day_of_week: DayOfWeek

    start_time: time

    end_time: time

    slot_duration: int = Field(
        default=15,
        ge=5,
        le=120
    )

    max_patients: int = Field(
        default=30,
        ge=1,
        le=500
    )


class DoctorScheduleUpdate(BaseModel):

    start_time: time | None = None

    end_time: time | None = None

    slot_duration: int | None = Field(
        default=None,
        ge=5,
        le=120
    )

    max_patients: int | None = Field(
        default=None,
        ge=1,
        le=500
    )

    is_active: bool | None = None


class DoctorScheduleResponse(BaseModel):

    schedule_id: str

    hospital_id: str

    doctor_id: str

    day_of_week: DayOfWeek

    start_time: time

    end_time: time

    slot_duration: int

    max_patients: int

    is_active: bool

    created_at: datetime

    updated_at: datetime