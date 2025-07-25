# MongoDB setup
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel,Field
from typing import List
from datetime import datetime,timezone
import asyncio
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["analysis_db"]
collection = db["agent_analysis"]


class CommentBy(BaseModel):
    name: str
    imageUrl: str


class Comment(BaseModel):
    response: str
    by: CommentBy
    date: str = datetime.now()

class AnalysisBase(BaseModel):
    agent: str="Crypto Agent"
    analysis: str="test"
    sentiment: str="test"
    analysis_type: str="daily_market_analysis"
    likes: int = 0
    view_count: int = 0
    comments: List[Comment] = []
    created_at: datetime = datetime.now(timezone.utc)  
    updated_at: datetime = datetime.now(timezone.utc)

        
        

    
async def addAnalysis(obj:AnalysisBase):
    # Convert Pydantic model to dictionary
    obj.created_at = datetime.now(timezone.utc)
    obj.updated_at = datetime.now(timezone.utc)
    print(obj)
    document = obj.model_dump(mode="python")
    # Insert document into MongoDB
    res = await collection.insert_one(document)
    print(res)
    return str(res.inserted_id)

