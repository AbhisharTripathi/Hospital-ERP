from datetime import datetime

from pydantic import BaseModel, Field

from app.models.stock import StockStatus


# ==========================================
# Create
# ==========================================

class StockCreate(BaseModel):

    medicine_id: str

    batch_id: str

    quantity: int = Field(
        gt=0
    )


# ==========================================
# Update
# ==========================================

class StockUpdate(BaseModel):

    quantity: int | None = Field(
        default=None,
        ge=0
    )

    reserved_quantity: int | None = Field(
        default=None,
        ge=0
    )

    status: StockStatus | None = None


# ==========================================
# Response
# ==========================================

class StockResponse(BaseModel):

    stock_id: str

    hospital_id: str

    medicine_id: str

    batch_id: str

    quantity: int

    reserved_quantity: int

    available_quantity: int

    status: StockStatus

    created_at: datetime

    updated_at: datetime