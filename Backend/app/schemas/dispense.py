from datetime import datetime
from pydantic import BaseModel


class DispensedBatch(BaseModel):
    medicine_id: str
    batch_id: str
    batch_number: str
    quantity: int


class DispensedMedicine(BaseModel):
    medicine_id: str
    medicine_name: str
    prescribed_quantity: int
    dispensed_quantity: int
    batches: list[DispensedBatch]


class DispenseResponse(BaseModel):
    prescription_id: str
    patient_id: str
    dispensed_by: str
    medicines: list[DispensedMedicine]
    dispensed_at: datetime