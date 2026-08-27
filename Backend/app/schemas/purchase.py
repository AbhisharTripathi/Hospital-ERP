from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.purchase import (
    PurchaseStatus
)


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
# Create Purchase
# ==========================================

class PurchaseCreate(BaseModel):

    supplier_id: str

    invoice_number: str = Field(
        min_length=1,
        max_length=100
    )

    invoice_date: date

    items: list[PurchaseItem] = Field(
        min_length=1
    )

    subtotal: float = Field(
        ge=0
    )

    discount: float = Field(
        default=0,
        ge=0
    )

    tax: float = Field(
        default=0,
        ge=0
    )

    total_amount: float = Field(
        ge=0
    )


# ==========================================
# Update Purchase
# ==========================================

class PurchaseUpdate(BaseModel):

    invoice_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    invoice_date: date | None = None

    discount: float | None = Field(
        default=None,
        ge=0
    )

    tax: float | None = Field(
        default=None,
        ge=0
    )


# ==========================================
# Status Update
# ==========================================

class PurchaseStatusUpdate(BaseModel):

    status: PurchaseStatus


# ==========================================
# Response
# ==========================================

class PurchaseResponse(BaseModel):

    purchase_id: str

    hospital_id: str

    supplier_id: str

    invoice_number: str

    invoice_date: date

    items: list[PurchaseItem]

    subtotal: float
    #{Subtotal} = {Quantity}*{Purchase Price} subtotal ka matlab hota hai Discount aur Tax apply hone se PEHLE ki kul rashi (Base Total).
    discount: float

    tax: float

    total_amount: float

    status: PurchaseStatus

    created_by: str

    created_at: datetime

    updated_at: datetime