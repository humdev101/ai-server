from ..models.collectionReviewModel import CollectionReviewModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta
from ..helpers.prompts import getCollectionReview
import os

MONGO_URL = os.getenv("MOBILE_MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["collection_review_agent"]
collection = db["collection_review"]

async def addCollectionReview(obj: CollectionReviewModel):
    # Convert Pydantic model to dictionary
    print(obj)
    document = obj.model_dump(mode="python")
    # Insert document into MongoDB
    res = await collection.insert_one(document)
    print(res)
    document["_id"] = str(document["_id"])
    return document    

async def getCollectionReviewDB(key: str,chain: str):
    # Find the document by ID
    try:
        document = await collection.find_one({"key": key,"chain": chain})
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
    

async def getCollectionReview1D(key: str,chain: str):
    # Find the document by ID
    try:
        docs = collection.find({"key": key,"chain": chain}).sort("created_at", -1).limit(1)
        document =None
        async for docu in docs:
            print("Document: ",document)
            document = docu
        if document:
            # Convert ObjectId to string
            document["_id"] = str(document["_id"])
            created_at = document["created_at"]
            created_at = created_at.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            print(f"Created At: {created_at}")
            time_difference = now - created_at
            if time_difference > timedelta(days=1):
                # Get AI analysis 
                ai_analysis = await getCollectionReview(key,chain,"llama3.1")
                #  create coin review object and return it
                coin_review_obj = CollectionReviewModel(
                    review=ai_analysis["data"],
                    rating=-1,
                    llm="llama3.1",
                    sentiment="-",
                    key=key,
                    chain=chain,
                    agent_name="collection_review_agent",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                doc = await addCollectionReview(coin_review_obj)
                print("Document is older than 1 day.")
                return doc
            else:
                print("Document is less than 1 day old.")
                print(document)
                return document
        else:
            ai_analysis = await getCollectionReview(key,chain,"llama3.1")
                #  create coin review object and return it
            coin_review_obj = CollectionReviewModel(
                    review=ai_analysis["data"],
                    rating=-1,
                    llm="llama3.1",
                    sentiment="-",
                    key=key,
                    chain=chain,
                    agent_name="collection_review_agent",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
            doc = await addCollectionReview(coin_review_obj)
            return doc
    except Exception as e:
        print(f"Error: {e}")
        return None