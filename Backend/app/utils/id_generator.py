from datetime import datetime
class IDGenerator:

    @staticmethod
    async def generate_patient_id(counter_repo):
        year = datetime.now().year
        seq = await counter_repo.get_next_sequence(f"patient:{year}")
        return f"PAT-{year}-{seq:05d}"
    
    @staticmethod
    async def generate_doctor_id(counter_repo):
        year = datetime.now().year
        seq = await counter_repo.get_next_sequence(f"doctor:{year}")
        return f"DOC-{year}-{seq:05d}"