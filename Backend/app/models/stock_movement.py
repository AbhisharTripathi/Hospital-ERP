from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Movement Type
# ==========================================

class StockMovementType(str, Enum):

    IN = "IN"

    OUT = "OUT"

    RETURN = "RETURN"

    ADJUSTMENT = "ADJUSTMENT"

    EXPIRED = "EXPIRED"


# ==========================================
# Stock Movement Model
# ==========================================

class StockMovementModel(BaseModel):

    movement_id: str

    hospital_id: str

    stock_id: str

    medicine_id: str

    batch_id: str

    movement_type: StockMovementType

    quantity: int = Field(
        gt=0
    )

    reference_type: str | None = None

    reference_id: str | None = None

    reason: str | None = None

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )