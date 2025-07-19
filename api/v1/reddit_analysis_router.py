# backend/routers/reddit_analysis_router.py
from pydantic import BaseModel
from api.adapters.reddit_adapter import search_reddit_items
from api.services.analyzer import analyze_items
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from db.crud.internet_post_crud import save_items_to_db
router = APIRouter()

class AnalyzeRequest(BaseModel):
    keyword: str
    max_count: int = 20

@router.post("/analyze_reddit")
async def analyze_reddit(data: AnalyzeRequest, db: Session = Depends(get_db)):
    items = await search_reddit_items(data.keyword, limit=data.max_count)
    if not items:
        return {"error": "No valid posts found"}

    # 保存到数据库
    save_items_to_db(items, db)

    result = await analyze_items(items)

    return {
        "keyword": data.keyword,
        "post_count": len(items),
        "analysis": result,
        "raw_items": [item.dict() for item in items]
    }
