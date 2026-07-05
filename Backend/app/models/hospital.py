from datetime import datetime,timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
class SubscriptionPlan(str, Enum):
    FREE = "FREE"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"

class SubscriptionStatus(str, Enum):
    TRIAL = "TRIAL"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"



class HospitalSettings(BaseModel):
    timezone: str = "Asia/Kolkata"
    currency: str = "INR"

class HospitalContact(BaseModel):
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None




class HospitalModel(BaseModel):
    hospital_id: str
    hospital_name:str #City General Hospital
    slug:str  #slug hospital ka url_friendly naam hai  slug= city-general-hospital
    owner_user_id: str|None=None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE
    subscription_status: SubscriptionStatus = SubscriptionStatus.TRIAL
    registered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    settings: HospitalSettings = Field(
        default_factory=HospitalSettings
    )
    contact: HospitalContact | None = None

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )