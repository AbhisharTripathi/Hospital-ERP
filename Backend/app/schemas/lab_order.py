from datetime import (
    date,
    datetime
)

from pydantic import (
    BaseModel,
    Field
)

from app.models.lab_order import (

    LabOrderStatus,

    LabPriority,

    LabTest

)


# ==========================================
# Create
# ==========================================

class LabOrderCreate(BaseModel):

    appointment_id: str

    

    tests: list[LabTest] = Field(

        min_length=1

    )

    priority: LabPriority = LabPriority.ROUTINE

    clinical_notes: str | None = Field(

        default=None,

        max_length=3000

    )

    expected_date: date | None = None


# ==========================================
# Update
# ==========================================

class LabOrderUpdate(BaseModel):

    tests: list[LabTest] | None = None

    priority: LabPriority | None = None

    clinical_notes: str | None = Field(

        default=None,

        max_length=3000

    )

    expected_date: date | None = None


# ==========================================
# Status Update
# ==========================================

class LabOrderStatusUpdate(BaseModel):

    status: LabOrderStatus


# ==========================================
# Upload Report
# ==========================================

class LabReportUpload(BaseModel):

    report_file: str


# ==========================================
# Response
# ==========================================

class LabOrderResponse(BaseModel):

    lab_order_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    tests: list[LabTest]

    priority: LabPriority

    clinical_notes: str | None

    expected_date: date | None

    status: LabOrderStatus

    report_file: str | None

    created_at: datetime

    updated_at: datetime