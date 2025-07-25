from motor.motor_asyncio import AsyncIOMotorClient
from ..models.mobileReviewModel import MobileReview
from ..helpers.prompts import getMobilePhoneReview
from bson import ObjectId
import os

MONGO_URL = os.getenv("MOBILE_MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["devices_review_agent"]
collection = db["device_review"]

async def getDeviceReview(device_id: str):
    # Find the document by ID
    try:
        print(device_id)
        document = await collection.find_one({"deviceId": device_id})
        if document:
            # Convert ObjectId to string
            document["_id"] = str(document["_id"])
            print(document)
            return document
        else:
            # Review device and save to database
            device_review = await getMobilePhoneReview(device_id,"llama3.1")
            # Create a new MobileReviewBase object
            review_obj = MobileReview(
                deviceId=device_id,
                review=device_review["data"],
                llm="llama3.1",
                sentiment="-",
                agent_name="GadgetGuru",
                rating=-1,
                mobile=device_review["mobile"],
            )
            document = review_obj.model_dump(mode="python")
            res = await collection.insert_one(document)
            print(res)
            document["_id"] = str(document["_id"])
            return document
    except Exception as e:
        print(f"Error: {e}")
        return None