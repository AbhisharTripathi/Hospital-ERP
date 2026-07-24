from datetime import (
    datetime,
    date,
    timezone
)

from enum import Enum

from pydantic import (
    BaseModel,
    Field
)


# ==========================================
# Order Status
# ==========================================

class LabOrderStatus(str, Enum):

    ORDERED = "ORDERED"

    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"

    IN_PROGRESS = "IN_PROGRESS"

    COMPLETED = "COMPLETED"

    REPORT_UPLOADED = "REPORT_UPLOADED"

    CANCELLED = "CANCELLED"


# ==========================================
# Test Priority
# ==========================================

class LabPriority(str, Enum):

    ROUTINE = "ROUTINE"

    URGENT = "URGENT"

    STAT = "STAT"


# ==========================================
# Single Test
# ==========================================

class LabTest(BaseModel):

    test_name: str

    instructions: str | None = None


# ==========================================
# Lab Order Model
# ==========================================

class LabOrderModel(BaseModel):

    lab_order_id: str

    hospital_id: str

    appointment_id: str

    patient_id: str

    doctor_id: str

    tests: list[LabTest]

    priority: LabPriority = LabPriority.ROUTINE

    clinical_notes: str | None = None

    expected_date: date | None = None

    status: LabOrderStatus = LabOrderStatus.ORDERED

    ordered_by: str

    report_file: str | None = None

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