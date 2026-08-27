from datetime import datetime

from pydantic import BaseModel,Field

# ==========================================
# Create
# ==========================================

class SupplierCreate(BaseModel):

    supplier_name:str=Field(
        min_length=2,
        max_length=150
    )
    contact_person:str|None=Field(
        default=None,
        max_length=100
    )

    phone:str|None=Field(
        default=None,
        max_length=20
    )
    email:str|None=Field(
        default=None,
        max_length=150
    )
    address:str|None=Field(
        default=None,
        max_length=300
    )

    gst_number:str=Field(
        default=None,
        max_length=30
    )

# ==========================================
# Update
# ==========================================
class SupplierUpdate(BaseModel):
    supplier_name :str| None=Field(
        default=None,
        min_length=2,
        max_length=150
    )

    contact_person:str|None=Field(
        default=None,
        max_length=100
    )

    phone:str|None=Field(
        default=None,
        max_length=20
    )

    email:str|None=Field(
        default=None,
        max_length=150
    )

    address:str|None=Field(
        default=None,
        max_length=300
    )

    gst_number:str|None=Field(
        default=None,
        max_length=30
    )

# ==========================================
# Response
# ==========================================

class SupplierResponse(BaseModel):

    supplier_id:str

    hospital_id:str

    supplier_name:str

    contact_person:str|None

    phone:str|None

    email:str|None

    address:str|None

    gst_number:str|None

    is_active:bool

    created_at:datetime

    updated_at:datetime
