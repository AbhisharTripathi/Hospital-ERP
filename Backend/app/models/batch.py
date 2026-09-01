from datetime import date, datetime, timezone

from pydantic import BaseModel, Field
from enum import Enum

class BatchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class BatchModel(BaseModel):

    batch_id: str

    hospital_id: str

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

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )