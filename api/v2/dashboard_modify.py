from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from db.models.dashboard_model import MonitorTask
from db.database import get_db
from api.auth.dependencies import get_current_user
from pydantic import BaseModel
from typing import List

class MonitorUpdate(BaseModel):
    name: Optional[str]
    frequency: Optional[str]
    keywords: Optional[List[str]]
    platforms: Optional[List[str]]

router = APIRouter()

@router.put("/monitors/{monitor_id}")
def update_monitor(
    monitor_id: int,
    monitor_update: MonitorUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    monitor = db.query(MonitorTask).filter(
        MonitorTask.id == monitor_id,
        MonitorTask.user_id == current_user.id
    ).first()

    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor not found")

    # 动态赋值，只有传了的才更新
    if monitor_update.name is not None:
        monitor.name = monitor_update.name
    if monitor_update.frequency is not None:
        monitor.frequency = monitor_update.frequency
    if monitor_update.keywords is not None:
        monitor.keywords = monitor_update.keywords
    if monitor_update.platforms is not None:
        monitor.platforms = monitor_update.platforms

    db.commit()
    db.refresh(monitor)

    return {
        "id": monitor.id,
        "name": monitor.name,
        "frequency": monitor.frequency,
        "keywords": monitor.keywords,
        "platforms": monitor.platforms,
        "status": monitor.status.value,
        "sentiment": monitor.sentiment,
        "mentions": monitor.mentions,
        "trend": monitor.trend,
        "lastUpdate": monitor.lastUpdate,
    }
