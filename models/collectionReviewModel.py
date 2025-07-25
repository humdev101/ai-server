from pydantic import BaseModel,Field
from datetime import datetime,timezone

class CollectionReviewModel(BaseModel):
    review: str
    rating: int
    llm: str
    sentiment: str
    key: str
    chain: str
    agent_name: str
    created_at: datetime = datetime.now(timezone.utc)  
    updated_at: datetime = datetime.now(timezone.utc)