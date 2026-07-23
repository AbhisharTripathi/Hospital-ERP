from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


# ==========================================
# Payment Status
# ==========================================

class PaymentStatus(str, Enum):

    PENDING = "PENDING"

    PARTIAL = "PARTIAL"

    PAID = "PAID"

    CANCELLED = "CANCELLED"


# ==========================================
# Payment Method
# ==========================================

class PaymentMethod(str, Enum):

    CASH = "CASH"

    CARD = "CARD"

    UPI = "UPI"

    NET_BANKING = "NET_BANKING"

    INSURANCE = "INSURANCE"


# ==========================================
# Bill Item Type
# ==========================================

class BillItemType(str, Enum):

    CONSULTATION = "CONSULTATION"

    MEDICINE = "MEDICINE"

    LAB = "LAB"

    PROCEDURE = "PROCEDURE"

    ROOM = "ROOM"

    OTHER = "OTHER"
    # baad me x ray injection aur bhi add kar sakte hai

# ==========================================
# Bill Item
# ==========================================

class BillItemModel(BaseModel):

    item_name: str

    item_type: BillItemType

    quantity: int = Field(
        ge=1
    )

    unit_price: float = Field(
        ge=0
    )

    total_price: float = Field(
        ge=0
    )


# ==========================================
# Billing Model
# ==========================================

class BillingModel(BaseModel):

    bill_id: str

    invoice_number: str

    hospital_id: str

    patient_id: str

    doctor_id: str

    appointment_id: str | None = None

    items: list[BillItemModel]

    subtotal: float

    discount: float = 0

    tax: float = 0

    grand_total: float

    payment_status: PaymentStatus = PaymentStatus.PENDING

    payment_method: PaymentMethod | None = None

    remarks: str | None = None

    created_by: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )