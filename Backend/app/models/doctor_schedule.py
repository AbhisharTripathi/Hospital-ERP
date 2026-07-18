from datetime import datetime, time, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DayOfWeek(str, Enum):

    MONDAY = "MONDAY"

    TUESDAY = "TUESDAY"

    WEDNESDAY = "WEDNESDAY"

    THURSDAY = "THURSDAY"

    FRIDAY = "FRIDAY"

    SATURDAY = "SATURDAY"

    SUNDAY = "SUNDAY"


class DoctorScheduleModel(BaseModel):

    schedule_id: str

    hospital_id: str

    doctor_id: str

    day_of_week: DayOfWeek

    start_time: time

    end_time: time

    slot_duration: int = 15

    max_patients: int = 30

    is_active: bool = True

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )