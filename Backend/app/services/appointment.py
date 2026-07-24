from datetime import datetime

from fastapi import HTTPException, status

from app.models.appointment import (
    AppointmentModel,
    AppointmentStatus
)

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentStatusUpdate
)

from app.repositories.appointment import (
    AppointmentRepository
)

from app.repositories.patient import (
    PatientRepository
)

from app.repositories.doctor import (
    DoctorRepository
)

from app.repositories.doctor_schedule import (
    DoctorScheduleRepository
)

from app.repositories.counters import (
    CountersRepository
)

from app.utils.id_generator import (
    IDGenerator
)


class AppointmentService:

    def __init__(
        self,
        appointment_repository: AppointmentRepository,
        patient_repository: PatientRepository,
        doctor_repository: DoctorRepository,
        schedule_repository: DoctorScheduleRepository,
        counter_repository: CountersRepository
    ):

        self.appointment_repo = appointment_repository
        self.patient_repo = patient_repository
        self.doctor_repo = doctor_repository
        self.schedule_repo = schedule_repository
        self.counter_repo = counter_repository

    # --------------------------------------------------
    # Response Builder
    # --------------------------------------------------

    def _build_response(
        self,
        appointment: dict
    ):

        return AppointmentResponse(

            appointment_id=appointment["appointment_id"],

            hospital_id=appointment["hospital_id"],

            patient_id=appointment["patient_id"],

            doctor_id=appointment["doctor_id"],

            department_id=appointment["department_id"],

            schedule_id=appointment["schedule_id"],

            appointment_date=appointment["appointment_date"],

            appointment_time=appointment["appointment_time"],

            token_number=appointment["token_number"],

            appointment_type=appointment["appointment_type"],

            status=appointment["status"],

            reason=appointment.get("reason"),

            notes=appointment.get("notes"),

            created_at=appointment["created_at"],

            updated_at=appointment["updated_at"]

        )

    # --------------------------------------------------
    # Create Appointment
    # --------------------------------------------------

    async def create_appointment(
        self,
        current_user,
        appointment_data: AppointmentCreate
    ):

        hospital_id = current_user["hospital_id"]

        # ---------------- Patient Validation ----------------

        patient = await self.patient_repo.get_patient_by_id(

            hospital_id=hospital_id,

            patient_id=appointment_data.patient_id

        )

        if not patient:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Patient not found"

            )

        # ---------------- Doctor Validation ----------------

        doctor = await self.doctor_repo.get_doctor_by_id(

            doctor_id=appointment_data.doctor_id,

            hospital_id=hospital_id

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )
        
        doctor_name = (
            doctor.get("full_name")
            or doctor.get("name")
            or f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
            or "Doctor"
        )

        patient_name = (
            patient.get("full_name")
            or patient.get("name")
            or f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
            or "Patient"
        )


        # ---------------- Doctor Schedule ----------------

        day_name = appointment_data.appointment_date.strftime(
            "%A"
        ).upper()

        schedules = await self.schedule_repo.get_by_day(

            hospital_id=hospital_id,

            doctor_id=appointment_data.doctor_id,

            day_of_week=day_name

        )

        if not schedules:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Doctor is not available on this day"

            )

        selected_schedule = None

        for schedule in schedules:

            if (

                schedule["start_time"]

                <=

                appointment_data.appointment_time.strftime("%H:%M")

                <

                schedule["end_time"]

            ):

                selected_schedule = schedule

                break

        if selected_schedule is None:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Doctor is not available at this time"

            )

        # ---------------- Slot Already Booked ----------------
        # Agar appointment_date 'date' object hai:
   
        date_str = (
            appointment_data.appointment_date.strftime("%Y-%m-%d")
            if hasattr(appointment_data.appointment_date, "strftime")
            else str(appointment_data.appointment_date)
        )

        time_str = (
            appointment_data.appointment_time.strftime("%H:%M:%S")
            if hasattr(appointment_data.appointment_time, "strftime")
            else str(appointment_data.appointment_time)
        )

        booked = await self.appointment_repo.get_by_slot(
            hospital_id=hospital_id,
            doctor_id=appointment_data.doctor_id,
            appointment_date=date_str,
            appointment_time=time_str
        )
        if booked:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Slot already booked"

            )

        # ---------------- Max Patient Validation ----------------

        appointments = await self.appointment_repo.get_appointments_by_day(

            hospital_id=hospital_id,

            doctor_id=appointment_data.doctor_id,

            appointment_date=appointment_data.appointment_date

        )

        if len(appointments) >= selected_schedule["max_patients"]:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Maximum appointments reached"

            )

        # ---------------- Token Number ----------------

        last_token = await self.appointment_repo.get_last_token(

            hospital_id=hospital_id,

            doctor_id=appointment_data.doctor_id,

            appointment_date=date_str

        )

        token_number = 1

        if last_token:

            token_number = last_token["token_number"] + 1

        # ---------------- Appointment ID ----------------

        appointment_id = await IDGenerator.generate_appointment_id(

            self.counter_repo

        )

        # ---------------- Model ----------------

        appointment_model = AppointmentModel(

            appointment_id=appointment_id,

            hospital_id=hospital_id,

            patient_id=appointment_data.patient_id,

            doctor_id=appointment_data.doctor_id,

            department_id=appointment_data.department_id,

            schedule_id=selected_schedule["schedule_id"],

            patient_name=patient_name,

            doctor_name=doctor_name,

            appointment_date=appointment_data.appointment_date,

            # appointment_time=appointment_data.appointment_time.strftime(
            #     "%H:%M"
            # ),
            appointment_time=appointment_data.appointment_time,

            token_number=token_number,

            appointment_type=appointment_data.appointment_type,

            reason=appointment_data.reason,

            notes=appointment_data.notes,

            created_by=current_user["user_id"]

        )

        await self.appointment_repo.create_appointment(

            appointment_model.model_dump(mode="json")

        )

        return self._build_response(

            appointment_model.model_dump(mode="json")

        )
    
    # --------------------------------------------------
    # Get All Appointments
    # --------------------------------------------------

    async def get_all_appointments(
        self,
        current_user,
        page: int = 1,
        limit: int = 20,
        search: str | None = None,
        doctor_id: str | None = None,
        patient_id: str | None = None,
        status: AppointmentStatus | None = None,
        appointment_date=None,
        sort_by: str = "appointment_date",
        sort_order: int = -1
    ):

        result = await self.appointment_repo.get_all_appointments(

            hospital_id=current_user["hospital_id"],

            page=page,

            limit=limit,

            search=search,

            doctor_id=doctor_id,

            patient_id=patient_id,

            status=status,

            appointment_date=appointment_date,

            sort_by=sort_by,

            sort_order=sort_order

        )

        appointments = [

            self._build_response(item)

            for item in result["items"]

        ]

        return {

            "items": appointments,

            "total": result["total"],

            "page": page,

            "limit": limit,

            "total_pages": (
                result["total"] + limit - 1
            ) // limit

        }

    # --------------------------------------------------
    # Get Appointment By ID
    # --------------------------------------------------

    async def get_appointment_by_id(
        self,
        current_user,
        appointment_id: str
    ):

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        return self._build_response(
            appointment
        )

    # --------------------------------------------------
    # Update Appointment
    # --------------------------------------------------

    async def update_appointment(
        self,
        current_user,
        appointment_id: str,
        appointment_data: AppointmentUpdate
    ):
        appointment = await self.appointment_repo.get_by_appointment_id(
            hospital_id=current_user["hospital_id"],
            appointment_id=appointment_id
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        # mode="json" se dates ("YYYY-MM-DD") aur time values direct string ban jati hain
        update_data = appointment_data.model_dump(
            exclude_unset=True,
            mode="json"
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nothing to update"
            )

        # Agar appointment_time string ki jagah time object ho, toh safest check:
        if update_data.get("appointment_time") is not None:
            time_val = update_data["appointment_time"]
            if hasattr(time_val, "strftime"):
                update_data["appointment_time"] = time_val.strftime("%H:%M")

        # Repository call
        await self.appointment_repo.update_appointment(
            hospital_id=current_user["hospital_id"],
            appointment_id=appointment_id,
            update_data=update_data
        )

        updated = await self.appointment_repo.get_by_appointment_id(
            hospital_id=current_user["hospital_id"],
            appointment_id=appointment_id
        )

        return self._build_response(updated)

    # --------------------------------------------------
    # Update Status
    # --------------------------------------------------

    async def update_status(
        self,
        current_user,
        appointment_id: str,
        status_data: AppointmentStatusUpdate
    ):

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        await self.appointment_repo.update_status(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id,

            status=status_data.status

        )

        updated = await self.appointment_repo.get_by_appointment_id(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id

        )

        return self._build_response(updated)

    # --------------------------------------------------
    # Delete Appointment
    # --------------------------------------------------

    async def delete_appointment(
        self,
        current_user,
        appointment_id: str
    ):

        appointment = await self.appointment_repo.get_by_appointment_id(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id

        )

        if not appointment:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Appointment not found"

            )

        await self.appointment_repo.delete_appointment(

            hospital_id=current_user["hospital_id"],

            appointment_id=appointment_id

        )

        return {

            "message": "Appointment deleted successfully"

        }
    

 