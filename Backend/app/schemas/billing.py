from datetime import datetime

from pydantic import BaseModel, Field

from app.models.billing import (
    BillItemType,
    PaymentMethod,
    PaymentStatus
)


# ==========================================
# Bill Item
# ==========================================

class BillItemCreate(BaseModel):

    item_name: str = Field(
        min_length=1,
        max_length=100
    )

    item_type: BillItemType

    quantity: int = Field(
        ge=1
    )

    unit_price: float = Field(
        ge=0
    )


class BillItemResponse(BaseModel):

    item_name: str

    item_type: BillItemType

    quantity: int

    unit_price: float

    total_price: float


# ==========================================
# Create Bill
# ==========================================

class BillingCreate(BaseModel):

    

    appointment_id: str | None = None

    items: list[BillItemCreate]

    discount: float = Field(
        default=0,
        ge=0
    )

    tax: float = Field(
        default=0,
        ge=0
    )

    payment_method: PaymentMethod | None = None

    remarks: str | None = Field(
        default=None,
        max_length=500
    )


# ==========================================
# Update Bill
# ==========================================

class BillingUpdate(BaseModel):

    items: list[BillItemCreate] | None = None

    discount: float | None = Field(
        default=None,
        ge=0
    )

    tax: float | None = Field(
        default=None,
        ge=0
    )

    payment_method: PaymentMethod | None = None

    remarks: str | None = Field(
        default=None,
        max_length=500
    )


# ==========================================
# Update Payment Status
# ==========================================

class BillingStatusUpdate(BaseModel):

    payment_status: PaymentStatus


# ==========================================
# Response
# ==========================================

class BillingResponse(BaseModel):

    bill_id: str

    invoice_number: str

    hospital_id: str

    patient_id: str

    doctor_id: str

    appointment_id: str | None

    items: list[BillItemResponse]

    subtotal: float

    discount: float

    tax: float

    grand_total: float

    payment_status: PaymentStatus

    payment_method: PaymentMethod | None

    remarks: str | None

    created_by: str

    created_at: datetime

    updated_at: datetime