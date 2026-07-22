from datetime import datetime, timezone
import math
from fastapi import HTTPException, status

from app.models.doctor import (
    DoctorModel,
    DoctorStatus
)

from app.models.user import (
    
    UserRole,
    UserStatus
)

from app.schemas.doctor import (
    DoctorCreate,
    DoctorResponse,
    DoctorUpdate,
    UpdateDoctorStatus
)

from app.schemas.pagination import (
    PaginatedResponse,
    build_pagination_meta
)

from app.repositories.doctor import DoctorRepository
from app.repositories.user import UserRepository
from app.repositories.department import DepartmentRepository
from app.repositories.counters import CountersRepository
from app.utils.id_generator import IDGenerator
from app.services.email import EmailService

class DoctorService:

    ALLOWED_SORT_FIELDS = {
        "created_at",
        "joining_date",
        "experience_years",
        "consultation_fee",
        "specialization",
        "qualification",
        "license_number"
    }
    
    def __init__(
        self,
        doctor_repository: DoctorRepository,
        user_repository: UserRepository,
        department_repository: DepartmentRepository,
        counter_repository: CountersRepository,
        email_service: EmailService
    ):

        self.doctor_repo = doctor_repository
        self.user_repo = user_repository
        self.department_repo = department_repository
        self.counter_repo = counter_repository
        self.email_service = email_service

    
    def _build_doctor_response(
        self,
        doctor,
        user
    ) -> DoctorResponse:

        return DoctorResponse(

            doctor_id=doctor["doctor_id"],

            user_id=user["user_id"],

            first_name=user["name"]["first"],

            last_name=user["name"].get("last"),

            email=user["email"],


            phone=user.get("contact",{}).get("phone"),

            # gender=doctor["gender"],
            gender=doctor.get("gender", "Not Specified"),

            department_id=doctor["department_id"],

            license_number=doctor["license_number"],

            qualification=doctor["qualification"],

            specialization=doctor["specialization"],

            experience_years=doctor["experience_years"],

            consultation_fee=doctor["consultation_fee"],

            joining_date=doctor["joining_date"],

            status=doctor["status"],

            created_at=doctor["created_at"],

            updated_at=doctor["updated_at"]

        )
    
    
    
    async def create_doctor_profile(
        self,
        doctor_data: DoctorCreate,
        current_user,
    ):
        user = await self.user_repo.get_by_user_id(
        doctor_data.user_id
        )

        if not user:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user["role"] != UserRole.DOCTOR:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected user is not a doctor"
            )
        
        if user["status"] != UserStatus.ACTIVE:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor account is not active"
            )
        
        department = await self.department_repo.get_by_department_id(

        department_id=doctor_data.department_id,

        hospital_id=user["hospital_id"]

        )

        if not department:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        if not department["is_active"]:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Department is inactive"

            )
        
        existing_license = await self.doctor_repo.get_by_license_number(

        hospital_id=user["hospital_id"],

        license_number=doctor_data.license_number

        )

        if existing_license:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="License number already exists"

            )
        existing_profile = await self.doctor_repo.get_by_user_id(

        hospital_id=user["hospital_id"],

        user_id=user["user_id"]

        )

        if existing_profile:

            raise HTTPException(

                status_code=status.HTTP_409_CONFLICT,

                detail="Doctor profile already exists"

            )
        
        doctor_id = await IDGenerator.generate_doctor_id(
        self.counter_repo
        )
        doctor_model = DoctorModel(

        doctor_id=doctor_id,

        user_id=user["user_id"],

        hospital_id=user["hospital_id"],
        
        gender=doctor_data.gender,

        department_id=doctor_data.department_id,

        license_number=doctor_data.license_number,

        qualification=doctor_data.qualification,

        specialization=doctor_data.specialization,

        experience_years=doctor_data.experience_years,

        consultation_fee=doctor_data.consultation_fee,

        joining_date=datetime.now(timezone.utc)
        )
        
        await self.doctor_repo.create_doctor(
        doctor_model.model_dump(mode="json")
        )
        try:
            await self.email_service.send_doctor_profile_created_email(
                doctor_name=user["name"]["first"],
                email=user["email"],
                doctor_id=doctor_model.doctor_id,
                department_name=department["name"],
                specialization=doctor_model.specialization
            )

        except Exception as e:
            print(f"Doctor welcome email failed: {e}")

        return self._build_doctor_response(
            doctor_model.model_dump(mode="json"),
            user
        )
    
    async def get_all_doctors(
        self,
        current_user,
        page:int =1,
        limit:int=20,
        search: str| None=None,
        department_id:str|None=None,
        doctor_status:DoctorStatus|None=None,
        sort_by: str="created_at",
        sort_order: int=-1,
       
    ):
        if sort_by not in self.ALLOWED_SORT_FIELDS:
            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail=f"Invalid sort field. Allowed fields: {', '.join(self.ALLOWED_SORT_FIELDS)}"

            )
        
        if sort_order not in (1, -1):
            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="sort_order must be either 1 (Ascending) or -1 (Descending)"

            )
        limit = max(10, min(limit, 100))
        page = max(page, 1)
        
        result = await self.doctor_repo.get_all_doctors(
            hospital_id=current_user["hospital_id"],
            page=page,
            limit=limit,
            search=search,
            department_id=department_id,
            status=doctor_status,
            sort_by=sort_by,
            sort_order=sort_order,
     

        )
        total = result["total"]
        
       

        response = []

        for doctor in result["items"]:
            
            user = await self.user_repo.get_by_user_id(
                doctor["user_id"]
            )

            if not user:
                continue

            response.append(
                self._build_doctor_response(
                    doctor,
                    user
                )
                    
            )
        pagination=build_pagination_meta(
            page=page,
            limit=limit,
            total_records=total,
          
            
        )

        return PaginatedResponse[DoctorResponse](
            data=response,
            pagination=pagination
        )
    
    async def get_doctor_by_id(
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

        user = await self.user_repo.get_by_user_id(
            doctor["user_id"]
        )

        return self._build_doctor_response(
            doctor,
            user
        )
    
    async def update_doctor(
        self,
        current_user,
        doctor_id: str,
        doctor_data: DoctorUpdate
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
        update_fields = doctor_data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        update_data = {}
        
        if "qualification" in update_fields:
            update_data["qualification"] = update_fields["qualification"]

        if "specialization" in update_fields:
            update_data["specialization"] = update_fields["specialization"] 

        if "experience_years" in update_fields:
            update_data["experience_years"] = update_fields["experience_years"] 
        
        if "consultation_fee" in update_fields:
            update_data["consultation_fee"] = update_fields["consultation_fee"]
        
        if "license_number" in update_fields:

            existing = await self.doctor_repo.get_by_license_number(
                hospital_id=current_user["hospital_id"],
                license_number=update_fields["license_number"]
            )

            if existing and existing["doctor_id"] != doctor_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="License number already exists"
                )

            update_data["license_number"] = update_fields["license_number"]

        if "department_id" in update_fields:

            department = await self.department_repo.get_by_department_id(
                department_id=update_fields["department_id"],
                hospital_id=current_user["hospital_id"]
            )

            if not department:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Department not found"
                )

            if not department["is_active"]:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Department is inactive"
                )

            update_data["department_id"] = update_fields["department_id"]
        
        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        await self.doctor_repo.update_doctor(
            doctor_id=doctor_id,
            hospital_id=current_user["hospital_id"],
            update_data=update_data
        )
        doctor = await self.doctor_repo.get_doctor_by_id(
            doctor_id=doctor_id,
            hospital_id=current_user["hospital_id"]
        )

        user = await self.user_repo.get_by_user_id(
            doctor["user_id"]
        )
        return self._build_doctor_response(
            doctor,
            user
        )
    


    async def update_doctor_status(
        self,
        current_user,
        doctor_id: str,
        status_data: UpdateDoctorStatus
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

        await self.doctor_repo.update_status(

            doctor_id=doctor_id,

            hospital_id=current_user["hospital_id"],

            status=status_data.status

        )

        doctor = await self.doctor_repo.get_doctor_by_id(

            doctor_id=doctor_id,

            hospital_id=current_user["hospital_id"]

        )

        user = await self.user_repo.get_by_user_id(
            doctor["user_id"]
        )

        return self._build_doctor_response(
            doctor,
            user
        )
    
    async def get_doctors_by_department(
        self,
        current_user,
        department_id: str
    ):
        department = await self.department_repo.get_by_department_id(

        department_id=department_id,

        hospital_id=current_user["hospital_id"]

        )

        if not department:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        doctors = await self.doctor_repo.get_by_department(

            hospital_id=current_user["hospital_id"],

            department_id=department_id

        )

        response = []

        for doctor in doctors:

            user = await self.user_repo.get_by_user_id(
                doctor["user_id"]
            )

            if not user:
                continue

            response.append(
                self._build_doctor_response(
                    doctor,
                    user
                )
            )

        return response