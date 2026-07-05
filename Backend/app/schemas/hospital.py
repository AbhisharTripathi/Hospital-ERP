from datetime import datetime
from app.models.user import UserRole
from pydantic import BaseModel, EmailStr, Field
from app.models.hospital import (
    HospitalContact,
    HospitalSettings,
    SubscriptionPlan,
    SubscriptionStatus,
)
class HospitalOwnerRegister(BaseModel):
    hospital_name: str = Field(
        min_length=2,
        max_length=100
    )

    owner_first_name: str = Field(
        min_length=2,
        max_length=50
    )

    owner_last_name: str | None = None

    owner_email: EmailStr

    owner_phone: str | None = Field(
        default=None,
        min_length=4,
        max_length=15
    )

    owner_password: str = Field(
        min_length=6,
        max_length=100
    )

 


class HospitalRegisterResponse(BaseModel):
    hospital_id: str
    owner_user_id: str
    hospital_name: str
    slug: str
    owner_email: str
    role: UserRole

    
class HospitalResponse(BaseModel):
    hospital_id: str

    hospital_name: str

    slug: str

    owner_user_id: str | None = None

    subscription_plan: SubscriptionPlan

    subscription_status: SubscriptionStatus

    settings: HospitalSettings

    contact: HospitalContact | None = None

    is_active: bool

    registered_at: datetime

    created_at: datetime

    updated_at: datetime


class HospitalUpdate(BaseModel):
    hospital_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    contact: HospitalContact | None = None

    settings: HospitalSettings | None = None

    subscription_plan: SubscriptionPlan | None = None

    subscription_status: SubscriptionStatus | None = None

    is_active: bool | None = None


