# routers/reddit_analysis_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from api.adapters.reddit_adapter import search_reddit_items
from api.services.analyzer_each_post import analyze_items_batch
from db.crud.internet_post_crud import save_items_to_db
from db.database import get_db

router = APIRouter()

class AnalyzeRequest(BaseModel):
    keyword: str
    max_count: int = 20

@router.post("/analyze_reddit_each")
async def analyze_reddit(data: AnalyzeRequest, db: Session = Depends(get_db)):
    items = await search_reddit_items(data.keyword, limit=data.max_count)
    if not items:
        return {"error": "No valid posts found"}

    save_items_to_db(items, db)

    result = await analyze_items_batch(items)

    return {
        "keyword": data.keyword,
        "post_count": len(items),
        "result": result  # contains 'aggregate' and 'per_item_results'
    }
