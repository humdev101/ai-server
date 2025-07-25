from pydantic import BaseModel,Field
from datetime import datetime,timezone

class NftReviewModel(BaseModel):
    review: str
    rating: int
    llm: str
    sentiment: str
    collection_key: str
    chain: str
    contract_address: str
    agent_name: str
    created_at: datetime = datetime.now(timezone.utc)  
    updated_at: datetime = datetime.now(timezone.utc)