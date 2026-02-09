from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client.cache_lab
collection = db.items

def seed_data(n=10000):
    if collection.count_documents({}) == 0:
        collection.insert_many(
            [{"_id": i, "value": f"value_{i}"} for i in range(n)]
        )

def get_from_db(key: int):
    return collection.find_one({"_id": key})
