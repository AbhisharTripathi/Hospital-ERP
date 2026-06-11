class PatientRepository:
    def __init__(self, db):
        self.db = db
    
    async def get_all_patients(self, limit=None):
        return await self.db.patients.find().to_list(limit)

    async def get_by_id(self, id):
        return await self.db.patients.find_one({"_id": id})
    
    async def delete_by_id(self, id):
        return await self.db.patients.delete_one({"_id": id})
    
    async def delete_all_patients(self):
        return await self.db.patients.delete_many({})
    
    async def update_by_id(self, id, updated_data ):
        return await self.db.patients.update_one({"_id": id}, {"$set" : updated_data})

    async def create_patient(self, patient_data):
        result = await self.db.patients.insert_one(patient_data)
        return result.inserted_id