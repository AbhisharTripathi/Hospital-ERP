from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.hospital import HospitalModel
from app.models.user import UserModel, UserRole, UserName, UserContact
from app.repositories.hospital import HospitalRepository
from app.repositories.user import UserRepository
from app.repositories.counters import CountersRepository
from app.schemas.hospital import HospitalOwnerRegister,HospitalRegisterResponse,SubscriptionPlan,HospitalContact,HospitalSettings
from app.utils.id_generator import IDGenerator
from app.utils.slug import generate_slug
from app.services.email import EmailService

class HospitalService:
    def __init__(
        self,
        hospital_repository: HospitalRepository,
        user_repository: UserRepository,
        counter_repository: CountersRepository,
        email_service:EmailService
    ):
        self.hospital_repo = hospital_repository
        self.user_repo = user_repository
        self.counter_repo = counter_repository
        self.email_service = email_service

    async def register_hospital_owner(
        self,
        register_data: HospitalOwnerRegister
    ):
        slug = generate_slug(
            register_data.hospital_name
        )

        existing_hospital = await self.hospital_repo.get_by_slug(
            slug
        )

        if existing_hospital:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hospital already exists with this name"
            )

        hospital_id = await IDGenerator.generate_hospital_id(
            self.counter_repo
        )

        owner_user_id = await IDGenerator.generate_user_id(
            self.counter_repo
        )

        existing_user = await self.user_repo.get_by_email(
            register_data.owner_email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Owner email already exists"
            )

        hashed_password = hash_password(
            register_data.owner_password
        )

        hospital_model = HospitalModel(
            hospital_id=hospital_id,
            hospital_name=register_data.hospital_name,
            slug=slug,
            owner_user_id=owner_user_id,
            subscription_plan=SubscriptionPlan.FREE,

            settings=HospitalSettings(),
            
            contact=HospitalContact(
            phone=register_data.owner_phone,
            email=register_data.owner_email
            )
           
        )

        user_model = UserModel(
            user_id=owner_user_id,
            hospital_id=hospital_id,
            name=UserName(
                first=register_data.owner_first_name,
                last=register_data.owner_last_name
            ),
            username=register_data.owner_email.split("@")[0],
            email=register_data.owner_email,
            password=hashed_password,
            role=UserRole.SUPER_ADMIN,
            is_password_set=True,
            contact=UserContact(
                phone=register_data.owner_phone
            ),
            permissions=[
                "admins:create",
                "admins:read",
                "admins:update",
                "users:read",
                "hospital:read",
                "hospital:update"
            ]
        )

        await self.hospital_repo.create_hospital(
            hospital_model.model_dump(mode="json")
        )

        await self.user_repo.create_user(
            user_model.model_dump(mode="json")
        )
        try:
            await self.email_service.send_welcome_email(
                owner_name=user_model.name.first,
                hospital_name=hospital_model.hospital_name,
                hospital_id=hospital_model.hospital_id,
                user_id=user_model.user_id,
                email=user_model.email
            )
        except Exception as e:
            print(f"welcome emil failed:{e}")

        return HospitalRegisterResponse(
            hospital_id=hospital_id,
            owner_user_id=owner_user_id,
            hospital_name=hospital_model.hospital_name,
            slug=hospital_model.slug,
            owner_email=user_model.email,
            role=user_model.role
        )