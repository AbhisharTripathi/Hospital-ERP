from pymongo import ReturnDocument

class CountersRepository:
    def __init__(self, db):
        self.db = db

    async def get_next_sequence(self, counter_id: str) -> int:
        
        counter = await self.db.counters.find_one_and_update(
            {"_id": counter_id},
            {"$inc": {"sequence": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER  # Safe for upserts!
        )
        return counter["sequence"]