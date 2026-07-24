import asyncio
from datetime import datetime
import zoneinfo

from app.repositories.dashboard import DashboardRepository

from app.schemas.dashboard import (
    DashboardHospital,
    DashboardStats,
    DashboardResponse,
    AppointmentStatusSummary,
    RecentAppointment
)


class DashboardService:

    def __init__(
        self,
        dashboard_repository: DashboardRepository
    ):

        self.dashboard_repo = dashboard_repository

    # ===========================================
    # Helper
    # ===========================================

    def _build_recent_appointment(
        self,
        appointment: dict
    ):

        return RecentAppointment(

            appointment_id=appointment["appointment_id"],

            patient_id=appointment["patient_id"],

            patient_name=appointment["patient_name"],

            doctor_id=appointment["doctor_id"],

            doctor_name=appointment["doctor_name"],

            appointment_time=str(
                appointment["appointment_time"]
            ),

            token_number=appointment["token_number"],

            status=appointment["status"]

        )

    # ===========================================
    # Admin Dashboard
    # ===========================================

    async def get_admin_dashboard(
        self,
        current_user
    ):

        hospital_id = current_user["hospital_id"]

        tz = zoneinfo.ZoneInfo(
            "Asia/Kolkata"
        )

        today = datetime.now(
            tz
        ).date()

        (
            hospital,

            total_patients,

            active_patients,

            total_doctors,

            active_doctors,

            total_departments,

            today_appointments,

            completed_today,

            cancelled_today,

            recent_appointments,

            status_summary

        ) = await asyncio.gather(

            self.dashboard_repo.get_hospital(
                hospital_id
            ),

            self.dashboard_repo.get_total_patients(
                hospital_id
            ),

            self.dashboard_repo.get_active_patients(
                hospital_id
            ),

            self.dashboard_repo.get_total_doctors(
                hospital_id
            ),

            self.dashboard_repo.get_active_doctors(
                hospital_id
            ),

            self.dashboard_repo.get_total_departments(
                hospital_id
            ),

            self.dashboard_repo.get_today_appointments(
                hospital_id,
                today
            ),

            self.dashboard_repo.get_today_completed(
                hospital_id,
                today
            ),

            self.dashboard_repo.get_today_cancelled(
                hospital_id,
                today
            ),

            self.dashboard_repo.get_recent_appointments(
                hospital_id
            ),

            self.dashboard_repo.get_status_summary(
                hospital_id,
                today
            )

        )
        # ===========================================
        # Appointment Status Summary
        # ===========================================

        summary = AppointmentStatusSummary()

        for item in status_summary:

            status = item["_id"]

            count = item["count"]

            if status == "BOOKED":
                summary.booked = count

            elif status == "CONFIRMED":
                summary.confirmed = count

            elif status == "CHECKED_IN":
                summary.checked_in = count

            elif status == "IN_PROGRESS":
                summary.in_progress = count

            elif status == "COMPLETED":
                summary.completed = count

            elif status == "CANCELLED":
                summary.cancelled = count

            elif status == "NO_SHOW":
                summary.no_show = count

        # ===========================================
        # Dashboard Cards
        # ===========================================

        stats = DashboardStats(

            total_patients=total_patients,

            active_patients=active_patients,

            total_doctors=total_doctors,

            active_doctors=active_doctors,

            total_departments=total_departments,

            today_appointments=today_appointments,

            completed_today=completed_today,

            cancelled_today=cancelled_today,

            today_revenue=0.0

        )

        # ===========================================
        # Recent Appointments
        # ===========================================

        recent = [

            self._build_recent_appointment(
                appointment
            )

            for appointment in recent_appointments

        ]

        # ===========================================
        # Final Response
        # ===========================================

        return DashboardResponse(

            hospital=DashboardHospital(

                hospital_id=hospital["hospital_id"],

                hospital_name=hospital["hospital_name"]

            ),

            stats=stats,

            recent_appointments=recent,

            appointment_status_summary=summary

        )