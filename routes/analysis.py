from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone



import os

router = APIRouter(
    prefix="/ai_analysis"
)

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["analysis_db"]
collection = db["agent_analysis"]




# Pydantic models

class CommentBy(BaseModel):
    name: str
    imageUrl: str


class Comment(BaseModel):
    response: str
    by: CommentBy
    date: str = datetime.now()



class AnalysisBase(BaseModel):
    agent: str="test"
    analysis: str="test"
    sentiment: str="test"
    analysis_type: str="test"
    likes: int = 0
    view_count: int = 0
    comments: List[Comment] = []
    created_at: str = datetime.now() 
    updated_at: str = datetime.now() 

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisResponse(AnalysisBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
        arbitrary_types_allowed = True

def to_bson(obj: BaseModel) -> dict:
    data = obj.model_dump(by_alias=True)
    # Optional: if any additional handling needed for nested ObjectId or datetime, do here
    return data
# Create analysis
@router.post("/analysis")
async def create_analysis(data: AnalysisBase):
    print(data)
    # bson_doc = to_bson(data)
    json_str = data.model_dump()
    print(json_str)
    res = await collection.insert_one(json_str)
    # created = await collection.find_one({"_id": res.inserted_id})
    return str(json_str)

# Get one analysis
@router.get("/analysis/{id}")
async def get_analysis(id: str):
    analysis = await collection.find_one({"_id": ObjectId(id)})
    if not analysis:
        raise HTTPException(status_code=404, detail="Item not found")
    analysis["_id"] = str(analysis["_id"])
    return analysis


# Get all
@router.get("/analysis")
async def list_analyses():
    cursor = collection.find().limit(5)
    analysisList =[]
    async for anal in cursor:
        anal["_id"] = str(anal["_id"])
        analysisList.append(anal)
    return analysisList



# Update
@router.put("/analysis/{id}", response_model=AnalysisResponse)
async def update_analysis(id: str, data: AnalysisCreate):
    update_data = data.dict()
    update_data["updated_at"] = datetime.utcnow()
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = await collection.find_one({"_id": ObjectId(id)})
    return updated


# Delete
@router.delete("/analysis/{id}")
async def delete_analysis(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}


# Stack-style list (latest analysis first)
@router.get("/analysisStack")
async def stack_analysis():
    cursor = collection.find().sort("created_at", -1).limit(1)
    value = None
    async for anal in cursor:
        print(cursor)
        if anal:
            value = anal
            value["_id"] = str(value["_id"])
    return value 