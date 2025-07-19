from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from db.database import get_db
from db.models.search_history_model import SearchHistory
from db.models.user import User  # 假设 user model 在这里
from pydantic import BaseModel
from api.v2.smart_search_analyze import analyze, AnalyzeRequest, SearchResultItem
from api.auth.dependencies import get_current_user  # 假设你的鉴权依赖在这里

router = APIRouter()

class SearchHistoryBase(BaseModel):
    query: str
    results_count: int
    sentiment: str
    platforms: List[str]
    analysis_result: Optional[dict]
    search_results: Optional[List[dict]]

class SearchHistoryCreateSchema(SearchHistoryBase):
    pass

class SearchHistorySchema(SearchHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


@router.get("/search_history", response_model=List[SearchHistorySchema])
def get_search_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == current_user.id)
        .order_by(SearchHistory.timestamp.desc())
        .all()
    )
    return records



@router.post("/search_history", response_model=SearchHistorySchema)
def create_search_history(
    item: SearchHistoryCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_item = SearchHistory(
        user_id=current_user.id,  # 注入当前登录用户ID
        query=item.query,
        timestamp=datetime.utcnow(),
        results_count=item.results_count,
        sentiment=item.sentiment,
        platforms=item.platforms,
        analysis_result=item.analysis_result,
        search_results=item.search_results,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/search_history/{history_id}/reanalyze")
async def reanalyze_history(history_id: int, db: Session = Depends(get_db)) -> Any:
    item = db.query(SearchHistory).filter(SearchHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    req = AnalyzeRequest(
        query=item.query,
        platforms=item.platforms,
        searchResults=[SearchResultItem(**sr) for sr in item.search_results]
    )

    new_analysis = await analyze(req)

    item.analysis_result = new_analysis.dict()
    item.timestamp = datetime.utcnow()
    item.sentiment = new_analysis.overall_sentiment.label
    db.commit()
    db.refresh(item)

    return {"status": "success", "newAnalysis": item.analysis_result}


@router.get("/search_history/{history_id}/download")
async def download_history(history_id: int, db: Session = Depends(get_db)):
    item = db.query(SearchHistory).filter(SearchHistory.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    content = {
        "id": item.id,
        "query": item.query,
        "timestamp": item.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "results_count": item.results_count,
        "sentiment": item.sentiment,
        "platforms": item.platforms,
        "analysis_result": item.analysis_result,
        "search_results": item.search_results,
    }

    return JSONResponse(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=search_history_{history_id}.json"}
    )
