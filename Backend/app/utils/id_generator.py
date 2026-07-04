from datetime import datetime
import zoneinfo 

class IDGenerator:

    @staticmethod
    async def generate_patient_id(counter_repo) -> str:
        
        tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        year = datetime.now(tz).year
        
        # MongoDB key: e.g., "patient:2026"
        seq = await counter_repo.get_next_sequence(f"patient:{year}")
        
        # Output: PAT-2026-00001
        return f"PAT-{year}-{seq:05d}"
    
    @staticmethod
    async def generate_user_id(
        counter_repo
    ) -> str:

        tz = zoneinfo.ZoneInfo(
            "Asia/Kolkata"
        )

        year = datetime.now(
            tz
        ).year

        seq = await counter_repo.get_next_sequence(
            f"user:{year}"
        )

        return f"USR-{year}-{seq:05d}"
    
    @staticmethod
    async def generate_doctor_id(
        counter_repo
    )->str:
        tz=zoneinfo.ZoneInfo(
            "Asia/Kolkata"
        )
        year=datetime.now(
            tz
        ).year

        seq= await counter_repo.get_next_sequence(
            f"doctor:{year}"
        )

        return f"DOC-{year}-{seq:05d}"