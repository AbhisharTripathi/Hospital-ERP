from pydantic import BaseModel

from app.models.appointment import AppointmentStatus


# ===========================
# Dashboard Cards
# ===========================

class DashboardStats(BaseModel):

    total_patients: int

    active_patients: int

    total_doctors: int

    active_doctors: int

    total_departments: int

    today_appointments: int

    completed_today: int

    cancelled_today: int

    today_revenue: float = 0.0


# ===========================
# Hospital Info
# ===========================

class DashboardHospital(BaseModel):

    hospital_id: str

    hospital_name: str


# ===========================
# Recent Appointment
# ===========================

class RecentAppointment(BaseModel):

    appointment_id: str

    patient_id: str

    patient_name: str

    doctor_id: str

    doctor_name: str

    appointment_time: str

    token_number: int

    status: AppointmentStatus


# ===========================
# Appointment Status Summary
# ===========================

class AppointmentStatusSummary(BaseModel): 
# for pie chart graph
    booked: int = 0

    confirmed: int = 0

    checked_in: int = 0

    in_progress: int = 0

    completed: int = 0

    cancelled: int = 0

    no_show: int = 0


# ===========================
# Dashboard Response
# ===========================

class DashboardResponse(BaseModel):

    hospital: DashboardHospital

    stats: DashboardStats

    recent_appointments: list[RecentAppointment]

    appointment_status_summary: AppointmentStatusSummary