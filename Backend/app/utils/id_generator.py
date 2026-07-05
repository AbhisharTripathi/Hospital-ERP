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