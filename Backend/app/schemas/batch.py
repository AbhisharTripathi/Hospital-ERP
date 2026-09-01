from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.batch import BatchStatus


# ==========================================
# Create Batch
# ==========================================

class BatchCreate(BaseModel):

    medicine_id: str

    batch_number: str = Field(
        min_length=1,
        max_length=100
    )

    expiry_date: date

    purchase_price: float = Field(
        ge=0
    )

    unit: str

    status: BatchStatus = BatchStatus.ACTIVE


# ==========================================
# Update Batch
# ==========================================

class BatchUpdate(BaseModel):

    expiry_date: date | None = None

    purchase_price: float | None = Field(
        default=None,
        ge=0
    )

    unit: str | None = None

    status: BatchStatus | None = None


# ==========================================
# Response
# ==========================================

class BatchResponse(BaseModel):

    batch_id: str

    hospital_id: str

    medicine_id: str

    batch_number: str

    expiry_date: date

    purchase_price: float

    unit: str

    status: BatchStatus

    created_at: datetime

    updated_at: datetime