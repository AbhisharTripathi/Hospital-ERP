from datetime import datetime

from pydantic import BaseModel, Field

from app.models.stock_movement import (
    StockMovementType
)


# ==========================================
# Create
# ==========================================

class StockMovementCreate(BaseModel):

    stock_id: str

    movement_type: StockMovementType

    quantity: int = Field(
        gt=0
    )

    reference_type: str | None = None

    reference_id: str | None = None

    reason: str | None = None


# ==========================================
# Response
# ==========================================

class StockMovementResponse(BaseModel):

    movement_id: str

    hospital_id: str

    stock_id: str

    medicine_id: str

    batch_id: str

    movement_type: StockMovementType

    quantity: int

    reference_type: str | None = None

    reference_id: str | None = None

    reason: str | None = None

    created_by: str

    created_at: datetime