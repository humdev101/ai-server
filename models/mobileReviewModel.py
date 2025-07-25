from pydantic import BaseModel,Field
from datetime import datetime,timezone

class MobileReview(BaseModel):
    review: str
    rating: int
    llm: str
    sentiment: str
    mobile: str
    deviceId: str
    agent_name: str
    created_at: datetime = datetime.now(timezone.utc)  
    updated_at: datetime = datetime.now(timezone.utc)