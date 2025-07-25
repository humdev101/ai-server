from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

MONGO_URL = os.getenv("MOBILE_MONGO_URL", "")
client = AsyncIOMotorClient(MONGO_URL)
db = client["devices"]
collection = db["devicecollections"]

async def getDevice(id: str):
    # Find the document by ID
    try:
        object_id = ObjectId(id)
        print(id)
        document = await collection.find_one({"_id": object_id})
        if document:
            # Convert ObjectId to string
            document["_id"] = str(document["_id"])
            print(document)
            return document
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None