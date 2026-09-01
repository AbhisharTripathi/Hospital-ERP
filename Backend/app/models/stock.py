from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Stock Status
# ==========================================

class StockStatus(str, Enum):

    AVAILABLE = "AVAILABLE"
    EXPIRED = "EXPIRED"
    BLOCKED = "BLOCKED"


# ==========================================
# Stock Model
# ==========================================

class StockModel(BaseModel):

    stock_id: str

    hospital_id: str

    medicine_id: str

    batch_id: str

    quantity: int = Field(
        ge=0
    )

    reserved_quantity: int = Field(
        default=0,
        ge=0
    )

    available_quantity: int = Field(
        ge=0
    )

    status: StockStatus = (
        StockStatus.AVAILABLE
    )

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )