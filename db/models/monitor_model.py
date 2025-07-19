from pydantic import BaseModel
from typing import List, Optional

class MonitorCreateRequest(BaseModel):
    name: str
    frequency: str
    keywords: str
    platforms: List[str]

class MonitorStatus(BaseModel):
    id: int
    name: str
    status: str
    sentiment: Optional[dict] = None
    mentions: Optional[int] = None
    trend: Optional[str] = None
    last_update: Optional[str] = None
