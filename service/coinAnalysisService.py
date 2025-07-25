# MongoDB setup
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from datetime import datetime,timezone
import os
from ..models.coinAnalysisModel import CoinAnalysisBase


MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["analysis_db"]
collection = db["coin_agent_analysis"]

    
async def addAnalysis(obj:CoinAnalysisBase):
    # Convert Pydantic model to dictionary
    obj.created_at = datetime.now(timezone.utc)
    obj.updated_at = datetime.now(timezone.utc)
    print(obj)
    document = obj.model_dump(mode="python")
    # Insert document into MongoDB
    res = await collection.insert_one(document)
    print(res)
    return str(res.inserted_id)

async def getAnalysisById(id: str):
    # Find the document by ID
    document = await collection.find_one({"_id": id})
    if document:
        # Convert ObjectId to string
        document["_id"] = str(document["_id"])
        return document
    else:
        return None
    
async def getAllAnalysis():
    # Find all documents
    cursor = collection.find()
    documents = []
    async for document in cursor:
        # Convert ObjectId to string
        document["_id"] = str(document["_id"])
        documents.append(document)
    return documents

async def stack_analysis_coin_analysis():
    cursor = collection.find().sort("created_at", -1).limit(1)
    value = None
    async for anal in cursor:
        print(cursor)
        if anal:
            value = anal
            value["_id"] = str(value["_id"])
    return value 