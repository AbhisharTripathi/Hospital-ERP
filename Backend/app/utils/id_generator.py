from datetime import datetime
import zoneinfo


class IDGenerator:
    @staticmethod
    def get_current_year() -> int:
        tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        return datetime.now(tz).year

    @staticmethod
    async def generate_patient_id(counter_repo) -> str:
        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"patient:{year}"
        )

        return f"PAT-{year}-{seq:05d}"

    @staticmethod
    async def generate_user_id(counter_repo) -> str:
        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"user:{year}"
        )

        return f"USR-{year}-{seq:05d}"

    @staticmethod
    async def generate_doctor_id(counter_repo) -> str:
        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"doctor:{year}"
        )

        return f"DOC-{year}-{seq:05d}"

    @staticmethod
    async def generate_hospital_id(counter_repo) -> str:
        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"hospital:{year}"
        )

        return f"HOSP-{year}-{seq:05d}"
    
    
    @staticmethod
    async def generate_department_id(counter_repo) -> str:
        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"department:{year}"
        )

        return f"DEP-{year}-{seq:05d}"
    
    @staticmethod
    async def generate_schedule_id(counter_repo) -> str:

        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"schedule:{year}"
        )

        return f"SCH-{year}-{seq:05d}"
    @staticmethod
    async def generate_appointment_id(counter_repo) -> str:

        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"appointment:{year}"
        )

        return f"APP-{year}-{seq:05d}"

    @staticmethod
    async def generate_bill_id(counter_repo) -> str:

        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(
            f"bill:{year}"
        )

        return f"BILL-{year}-{seq:05d}"
    @staticmethod
    async def generate_prescription_id(counter_repo) -> str:

        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(

            f"prescription:{year}"

        )

        return f"PX-{year}-{seq:05d}"
    @staticmethod
    async def generate_vital_id(
        counter_repo
    ) -> str:

        year = IDGenerator.get_current_year()

        seq = await counter_repo.get_next_sequence(

            f"vital:{year}"

        )

        return f"VIT-{year}-{seq:05d}"