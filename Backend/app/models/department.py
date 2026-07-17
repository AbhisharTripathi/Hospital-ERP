from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DepartmentModel(BaseModel):

    department_id: str

    hospital_id: str

    name: str = Field(
        min_length=2,
        max_length=100
    )

    code: str = Field(
        min_length=2,
        max_length=10
    )

    description: str | None = None

    head_doctor_id: str | None = None

    is_active: bool = True

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    