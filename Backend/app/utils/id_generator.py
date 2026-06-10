class IDGenerator:

    @staticmethod
    async def generate_patient_id(counter_repo):
        seq = await counter_repo.get_next_sequence("patient")
        return f"PAT-{seq:05d}"
    
    async def generate_doctor_id(counter_repo):
        seq = await counter_repo.get_next_sequence("doctor")
        return f"DOC-{seq:05d}"