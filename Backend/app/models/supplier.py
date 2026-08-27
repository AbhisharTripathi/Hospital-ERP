from datetime import datetime,timezone
from pydantic import BaseModel,Field

class SupplierModel(BaseModel):
    supplier_id:str
    hospital_id:str
    supplier_name: str= Field(
        min_length=2,
        max_length=150
    )

    contact_person:str|None= Field(
        default=None,
        max_length=100
    )
    phone:str |None =Field(
        default=None,
        max_length=20
    )
    email: str | None = Field(
        default=None,
        max_length=150
    )

    address:str=Field(
        default=None,
        max_length=300
    )

    gst_number:str =Field(
        default=None,
        max_length=30
    )

    is_active:bool=True
    created_by:str
    created_at:datetime=Field(
        default_factory=lambda:datetime.now(timezone.utc)
    )
    updated_at:datetime=Field(
        default_factory=lambda:datetime.now(timezone.utc)
    )
