from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalyzableItem(BaseModel):
    platform: str
    content: str
    author: str
    publish_time: datetime
    url: Optional[str] = None
    likes: Optional[int] = 0
    comments: Optional[int] = 0
    shares: Optional[int] = 0
