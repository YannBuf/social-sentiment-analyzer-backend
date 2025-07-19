from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db  # 你数据库session获取函数
from db.models.search_history_model import SearchHistory


router = APIRouter()

@router.get("/search_history/{history_id}/details")
def get_search_history_details(history_id: int, db: Session = Depends(get_db)):
    history = db.query(SearchHistory).filter(SearchHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Search history not found")

    # 直接从history.analysis_result取值，可能是个dict或JSON字符串，需要转换
    analysis_result = history.analysis_result
    if isinstance(analysis_result, str):
        import json
        try:
            analysis_result = json.loads(analysis_result)
        except Exception:
            analysis_result = None

    return {
        "search_history": {
            "id": history.id,
            "user_id": history.user_id,
            "query": history.query,
            "timestamp": history.timestamp,
            "results_count": history.results_count,
            "sentiment": history.sentiment,
            "platforms": history.platforms,
            "search_results": history.search_results,
        },
        "analysis_result": analysis_result or None,
    }
