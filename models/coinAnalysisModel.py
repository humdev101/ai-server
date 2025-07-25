from pydantic import BaseModel,Field
from typing import List
from datetime import datetime,timezone

class CommentBy(BaseModel):
    name: str
    imageUrl: str


class Comment(BaseModel):
    response: str
    by: CommentBy
    date: str = datetime.now()

class CoinAnalysisBase(BaseModel):
    agent: str="Crypto Agent"
    analysis: str="test"
    sentiment: str="test"
    analysis_type: str="daily_market_analysis"
    likes: int = 0
    view_count: int = 0
    comments: List[Comment] = []
    coin_name: str = "Bitcoin"
    coin_symbol: str = "BTCUSDT"
    timeframe: str = "3d"
    interval: str = "1h"
    created_at: datetime = datetime.now(timezone.utc)  
    updated_at: datetime = datetime.now(timezone.utc)
