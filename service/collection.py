from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

MONGO_URL = os.getenv("MOBILE_MONGO_URL", "mongodb+srv://staging_db:StagingDB-1@cluster0.cnrsg44.mongodb.net/")
client = AsyncIOMotorClient(MONGO_URL)
db = client["marketplace"]
collection = db["collections"]

async def getCollection(key: str,chain: str):
    # Find the document by ID
    try:
        print(key)
        document = await collection.find_one({"blockSpanKey": key,"chainType": chain})
        if document:
            # Convert ObjectId to string
            document["_id"] = str(document["_id"])
            print(document)
            # return document
            for link in document["socialLinks"]:
               link["_id"] = str(link["_id"])
            return document
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None