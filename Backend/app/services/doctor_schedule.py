from datetime import datetime,time

from fastapi import HTTPException, status

from app.models.doctor_schedule import (
    DoctorScheduleModel
)

from app.schemas.doctor_schedule import (
    DoctorScheduleCreate,
    DoctorScheduleUpdate,
    DoctorScheduleResponse
)

from app.repositories.doctor_schedule import (
    DoctorScheduleRepository
)

from app.repositories.doctor import (
    DoctorRepository
)

from app.repositories.counters import (
    CountersRepository
)

from app.utils.id_generator import (
    IDGenerator
)


class DoctorScheduleService:

    def __init__(
        self,
        schedule_repository: DoctorScheduleRepository,
        doctor_repository: DoctorRepository,
        counter_repository: CountersRepository
    ):

        self.schedule_repo = schedule_repository

        self.doctor_repo = doctor_repository

        self.counter_repo = counter_repository


    def _build_schedule_response(
        self,
        schedule: dict
    ):

        return DoctorScheduleResponse(

            schedule_id=schedule["schedule_id"],

            hospital_id=schedule["hospital_id"],

            doctor_id=schedule["doctor_id"],

            day_of_week=schedule["day_of_week"],

            start_time=schedule["start_time"],

            end_time=schedule["end_time"],

            slot_duration=schedule["slot_duration"],

            max_patients=schedule["max_patients"],

            is_active=schedule["is_active"],

            created_at=schedule["created_at"],

            updated_at=schedule["updated_at"]
        )
   
    
    async def create_schedule(
        self,
        current_user,
        schedule_data: DoctorScheduleCreate
    ):
        doctor = await self.doctor_repo.get_doctor_by_id(

            doctor_id=schedule_data.doctor_id,

            hospital_id=current_user["hospital_id"]

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )
        schedules = await self.schedule_repo.get_schedule_overlap(

                hospital_id=current_user["hospital_id"],

                doctor_id=schedule_data.doctor_id,

                day_of_week=schedule_data.day_of_week

        )
        def to_time(val):
                if isinstance(val, str):
                    return time.fromisoformat(val)
                return val
        for schedule in schedules:
            # High-level safety: Dono ko time object bana lo pehle
            s_start = to_time(schedule_data.start_time)
            s_end = to_time(schedule_data.end_time)
            
            db_start = to_time(schedule["start_time"])
            db_end = to_time(schedule["end_time"])

            # Ab clean comparison hoga, bina kisi TypeError ke:
            if s_start < db_end and s_end > db_start:
                raise HTTPException(
                    status_code=400,
                    detail="Doctor schedule overlaps with an existing schedule."
                )

                
        schedule_id = await IDGenerator.generate_schedule_id(
            self.counter_repo
        )

        schedule_model = DoctorScheduleModel(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"],

            doctor_id=schedule_data.doctor_id,

            day_of_week=schedule_data.day_of_week,

            start_time = schedule_data.start_time.strftime("%H:%M"),

            end_time=schedule_data.end_time.strftime("%H:%M"),

            slot_duration=schedule_data.slot_duration,

            max_patients=schedule_data.max_patients,

            created_by=current_user["user_id"]
        )
        await self.schedule_repo.create_schedule(

            schedule_model.model_dump(
                mode="json"
            )

        )
        return self._build_schedule_response(

            schedule_model.model_dump(
                mode="json"
            )

        )


    async def get_schedule_by_doctor(
        self,
        current_user,
        doctor_id: str
    ):

        doctor = await self.doctor_repo.get_doctor_by_id(

            doctor_id=doctor_id,

            hospital_id=current_user["hospital_id"]

        )

        if not doctor:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Doctor not found"

            )

        schedules = await self.schedule_repo.get_by_doctor(

            hospital_id=current_user["hospital_id"],

            doctor_id=doctor_id

        )

        return [

            self._build_schedule_response(schedule)

            for schedule in schedules

        ]

    async def get_schedule_by_id(
        self,
        current_user,
        schedule_id: str
    ):

        schedule = await self.schedule_repo.get_by_schedule_id(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        if not schedule:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Schedule not found"

            )

        return self._build_schedule_response(
            schedule
        )
    


    async def update_schedule(
        self,
        current_user,
        schedule_id: str,
        schedule_data: DoctorScheduleUpdate
    ):

        schedule = await self.schedule_repo.get_by_schedule_id(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        if not schedule:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Schedule not found"

            )

        update_data = schedule_data.model_dump(
            exclude_unset=True
        )

        if not update_data:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Nothing to update"

            )

        if "start_time" in update_data and update_data["start_time"] is not None:
            if hasattr(update_data["start_time"], "strftime"):
                update_data["start_time"] = update_data["start_time"].strftime("%H:%M")

        if "end_time" in update_data and update_data["end_time"] is not None:
            if hasattr(update_data["end_time"], "strftime"):
                update_data["end_time"] = update_data["end_time"].strftime("%H:%M")
        # -------------------------------------------------------

        doctor_id = schedule["doctor_id"]
        day = schedule["day_of_week"]

        start_time = update_data.get(
            "start_time",
            schedule["start_time"]
        )

        end_time = update_data.get(
            "end_time",
            schedule["end_time"]
        )

        overlaps = await self.schedule_repo.get_by_schedule_id_except_current(
            hospital_id=current_user["hospital_id"],
            doctor_id=doctor_id,
            day_of_week=day,
            schedule_id=schedule_id
        )

        for item in overlaps:
            if (
                start_time < item["end_time"]
                and
                end_time > item["start_time"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Schedule overlaps with existing schedule"
                )

        await self.schedule_repo.update_schedule(
            schedule_id=schedule_id,
            hospital_id=current_user["hospital_id"],
            update_data=update_data
        )

        updated = await self.schedule_repo.get_by_schedule_id(
            schedule_id=schedule_id,
            hospital_id=current_user["hospital_id"]
        )

        return self._build_schedule_response(updated)
    
        
    
    async def update_schedule_status(
        self,
        current_user,
        schedule_id: str,
        is_active: bool
    ):

        schedule = await self.schedule_repo.get_by_schedule_id(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        if not schedule:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Schedule not found"

            )

        await self.schedule_repo.update_status(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"],

            is_active=is_active

        )

        updated = await self.schedule_repo.get_by_schedule_id(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        return self._build_schedule_response(updated)
    
    async def delete_schedule(
        self,
        current_user,
        schedule_id: str
    ):

        schedule = await self.schedule_repo.get_by_schedule_id(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        if not schedule:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Schedule not found"

            )

        await self.schedule_repo.delete_schedule(

            schedule_id=schedule_id,

            hospital_id=current_user["hospital_id"]

        )

        return {

            "message": "Schedule deleted successfully"

        }