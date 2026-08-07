from datetime import datetime

from pydantic import BaseModel, Field

from app.models.medicine import (
    DosageForm,
    MedicineUnit
)


# ==========================================
# Create
# ==========================================

class MedicineCreate(BaseModel):

    medicine_name: str = Field(
        min_length=2,
        max_length=150
    )

    generic_name: str | None = Field(
        default=None,
        max_length=150
    )

    strength: str | None = Field(
        default=None,
        max_length=50
    )

    dosage_form: DosageForm

    manufacturer: str | None = Field(
        default=None,
        max_length=150
    )

    unit: MedicineUnit

    reorder_level: int = Field(
        default=0,
        ge=0
    )


# ==========================================
# Update
# ==========================================

class MedicineUpdate(BaseModel):

    medicine_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    generic_name: str | None = Field(
        default=None,
        max_length=150
    )

    strength: str | None = Field(
        default=None,
        max_length=50
    )

    dosage_form: DosageForm | None = None

    manufacturer: str | None = Field(
        default=None,
        max_length=150
    )

    unit: MedicineUnit | None = None

    reorder_level: int | None = Field(
        default=None,
        ge=0
    )


# ==========================================
# Response
# ==========================================

class MedicineResponse(BaseModel):

    medicine_id: str

    hospital_id: str

    medicine_name: str

    generic_name: str | None

    strength: str | None

    dosage_form: DosageForm

    manufacturer: str | None

    unit: MedicineUnit

    reorder_level: int

    is_active: bool

    created_by: str

    created_at: datetime

    updated_at: datetime