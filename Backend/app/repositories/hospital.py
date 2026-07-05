class HospitalRepository:
    def __init__(self,db):
        self.db=db
    
    async def create_hospital(
            self,
            hospital_data:dict
    ):
        result =await self.db.hospitals.insert_one(
            hospital_data
        )
        return result.inserted_id
    
    async def get_by_hospital_id(
            self,
            hospital_id:str
    ):
        return await self.db.hospitals.find_one(
            {
                "hospital_id":hospital_id
            }
        )
    
    async def get_by_slug(
            self,
            slug:str
    ):
        return await self.db.hospitals.find_one(
            {
                "slug":slug
            }
        )
    
    async def update_hospital(
            self,
            hospital_id:str,
            update_data:dict
    ):
        return await self.db.hospitals.update_one(
            {
                "hospital_id": hospital_id
            },
            {
                "$set":update_data
            }
        )
        
        