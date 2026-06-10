from app.schemas.patient import PatientCreate
from app.models.patient import PatientModel
from datetime import datetime
from app.utils.id_generator import IDGenerator
import bcrypt

class PatientServices:
    def __init__(self, patient_repository, counter_repository):
        self.patient_repo = patient_repository
        self.counter_repo = counter_repository

    async def create_patient(self, patient : PatientCreate):

        patient_id = await IDGenerator.generate_patient_id(self.counter_repo)

        if patient.password:
            raw_password = patient.password
        else :
            raw_password = patient.dob.strftime("%d%m%Y")

        encoded_hashed_password = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        hashed_password = encoded_hashed_password.decode("utf-8")

        patient = PatientModel(
            {
                **patient.model_dump(exclude={"password"}),
                "patient_id" : patient_id,
                "password" : hashed_password
            }
        )
        inserted_id = await self.patient_repo.create_patient(patient)
        return inserted_id