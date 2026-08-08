from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Dosage Form
# ==========================================

class DosageForm(str, Enum):

    TABLET = "TABLET"
    CAPSULE = "CAPSULE"
    SYRUP = "SYRUP"
    INJECTION = "INJECTION"
    CREAM = "CREAM"
    OINTMENT = "OINTMENT"
    DROPS = "DROPS"


# ==========================================
# Medicine Unit
# ==========================================

class MedicineUnit(str, Enum):

    TABLET = "TABLET"
    CAPSULE = "CAPSULE"
    BOTTLE = "BOTTLE"
    VIAL = "VIAL"
    TUBE = "TUBE"
    PIECE = "PIECE"


# ==========================================
# Medicine Model
# ==========================================

class MedicineModel(BaseModel):

    medicine_id: str

    hospital_id: str

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
    ) # wo minimum stock quantity jaha aphuchne per hospital ko nayi medicine order karne ka signal milta hai 

    is_active: bool = True

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )