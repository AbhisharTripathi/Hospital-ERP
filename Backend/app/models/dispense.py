from datetime import datetime, timezone
from pydantic import BaseModel, Field


class DispensedBatchModel(BaseModel):
    medicine_id: str
    batch_id: str
    batch_number: str
    quantity: int = Field(gt=0)


class DispensedMedicineModel(BaseModel):
    medicine_id: str
    medicine_name: str
    prescribed_quantity: int = Field(gt=0)
    dispensed_quantity: int = Field(gt=0)
    batches: list[DispensedBatchModel]


class DispenseModel(BaseModel):
    dispense_id: str
    hospital_id: str
    prescription_id: str
    patient_id: str
    dispensed_by: str
    medicines: list[DispensedMedicineModel]
    dispensed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )