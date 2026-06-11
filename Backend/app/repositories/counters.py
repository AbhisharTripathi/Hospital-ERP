from pymongo import ReturnDocument

class CountersRepository:
    def __init__(self, db):
        self.db = db

    async def get_next_sequence(self, id):
        counter = await self.db.counters.find_one_and_update(
            {"_id": id},
            {"$inc": {"sequence": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return counter["sequence"]