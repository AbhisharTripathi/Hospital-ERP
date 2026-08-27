from datetime import date, datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Purchase Status
# ==========================================

class PurchaseStatus(str, Enum):

    DRAFT = "DRAFT"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


# ==========================================
# Purchase Item
# ==========================================

class PurchaseItem(BaseModel):

    medicine_id: str

    batch_number: str = Field(
        min_length=1,
        max_length=100
    )

    expiry_date: date

    quantity: int = Field(
        gt=0
    )

    purchase_price: float = Field(
        ge=0
    )

    unit: str


# ==========================================
# Purchase Model
# ==========================================

class PurchaseModel(BaseModel):

    purchase_id: str

    hospital_id: str

    supplier_id: str

    invoice_number: str

    invoice_date: date

    items: list[PurchaseItem]

    subtotal: float

    discount: float = 0

    tax: float = 0

    total_amount: float

    status: PurchaseStatus = PurchaseStatus.DRAFT

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )