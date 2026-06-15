

class PatientRepository:
    def __init__(self, db):
        self.db = db
    
    async def create_patient(self, patient_data):
        result = await self.db.patients.insert_one(patient_data)
        return result.inserted_id
    
    async def get_all_patients(self, limit=None):
        return await self.db.patients.find().to_list(limit)
    
    async def search_patients(self, filters, limit=20):
       return await self.db.patients.find(filters).to_list(limit)

    
    
    async def get_by_patient_id(self, patient_id):
        return await self.db.patients.find_one({"patient_id": patient_id})
    
    async def get_by_phone(self, phone):
        return await self.db.patients.find_one({"phone": phone})    
    
    async def update_by_patient_id(self, patient_id, updated_data ):
        return await self.db.patients.update_one({"patient_id": patient_id}, {"$set" : updated_data})
    
    async def delete_by_patient_id(self, patient_id):
        return await self.db.patients.delete_one({"patient_id": patient_id})
    
    async def delete_all_patients(self):
        return await self.db.patients.delete_many({})
    
    


 
    
   