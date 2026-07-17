from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    code: str = Field(
        min_length=2,
        max_length=10
    )

    description: str | None = None


class DepartmentUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

   

    description: str | None = None

    head_doctor_id: str | None = None


class DepartmentResponse(BaseModel):

    department_id: str

    hospital_id: str

    name: str

    code: str

    description: str | None = None

    head_doctor_id: str | None = None

    is_active: bool
    # created_at: datetime
    # updated_at: datetime

class UpdateDepartmentStatus(BaseModel):

    is_active: bool