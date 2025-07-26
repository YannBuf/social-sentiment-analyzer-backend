from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random

from db.database import SessionLocal, engine, Base
from db.models.dashboard_model import MonitorTask, MonitorStatus
from pydantic import BaseModel
from typing import List, Dict
from api.auth.dependencies import get_db, get_current_user
from db.models.user import User


# 初始化建表
Base.metadata.create_all(bind=engine)

router = APIRouter()


class MonitorCreateRequest(BaseModel):
    name: str
    frequency: str
    keywords: str
    platforms: List[str]


class MonitorStatusResponse(BaseModel):
    status: str
    sentiment: Dict[str, int]
    mentions: int
    trend: str

class MonitorListItem(BaseModel):
    id: int
    name: str
    keywords: List[str]
    platforms: List[str]
    status: str
    sentiment: dict
    mentions: int
    trend: str
    lastUpdate: str

    model_config = {"from_attributes": True}

@router.get("/monitor/list", response_model=List[MonitorListItem])
def get_monitor_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(f"[monitor/list] current_user.id: {current_user.id}")
    monitors = (
        db.query(MonitorTask)
        .filter(MonitorTask.user_id == current_user.id)
        .all()
    )
    print(f"[monitor/list] 查询到 {len(monitors)} 条监控任务")

    # 补充 lastUpdate 字段，可以根据你的业务逻辑生成时间字符串
    def format_last_update(monitor: MonitorTask) -> str:
        # 假设用更新时间字段，或简单写死一个字符串
        return "Just updated"

    result = []
    for m in monitors:
        item = MonitorListItem.from_orm(m)
        item.lastUpdate = format_last_update(m)
        result.append(item)

    return result


@router.post("/monitor/create")
def create_monitor(
    req: MonitorCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = MonitorTask(
        name=req.name,
        frequency=req.frequency,
        keywords=[k.strip() for k in req.keywords.split(",")],
        platforms=req.platforms,
        status=MonitorStatus.processing,
        user_id=current_user.id,  # 绑定当前用户
    )
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"Monitor created successfully: id={task.id}, user_id={task.user_id}")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to create monitor: {e}")

    return {"task_id": task.id}


@router.get("/monitor/{monitor_id}/status", response_model=MonitorStatusResponse)
def get_monitor_status(
    monitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitor = (
        db.query(MonitorTask)
        .filter(MonitorTask.id == monitor_id, MonitorTask.user_id == current_user.id)
        .first()
    )

    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor task not found")

    if monitor.status == MonitorStatus.processing:
        # 模拟分析结果，实际请替换为真实业务逻辑
        positive = random.randint(50, 80)
        neutral = random.randint(10, 30)
        negative = 100 - (positive + neutral)

        monitor.sentiment = {
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
        }
        monitor.mentions = random.randint(500, 3000)
        monitor.trend = random.choice(["up", "down"])
        monitor.status = MonitorStatus.completed

        db.commit()

    return MonitorStatusResponse(
        status=monitor.status,
        sentiment=monitor.sentiment,
        mentions=monitor.mentions,
        trend=monitor.trend,
    )


@router.patch("/monitor/{monitor_id}/pause")
def pause_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitor = (
        db.query(MonitorTask)
        .filter(MonitorTask.id == monitor_id, MonitorTask.user_id == current_user.id)
        .first()
    )
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor task not found")

    if monitor.status == MonitorStatus.active:
        monitor.status = MonitorStatus.paused
        db.commit()
        return {"message": "Monitor paused"}
    return {"message": "Monitor is not active, cannot pause"}


@router.patch("/monitor/{monitor_id}/resume")
def resume_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitor = (
        db.query(MonitorTask)
        .filter(MonitorTask.id == monitor_id, MonitorTask.user_id == current_user.id)
        .first()
    )
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor task not found")

    if monitor.status == MonitorStatus.paused:
        monitor.status = MonitorStatus.active
        db.commit()
        return {"message": "Monitor resumed"}
    return {"message": "Monitor is not paused, cannot resume"}


@router.delete("/monitor/{monitor_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    monitor = (
        db.query(MonitorTask)
        .filter(MonitorTask.id == monitor_id, MonitorTask.user_id == current_user.id)
        .first()
    )
    if not monitor:
        raise HTTPException(status_code=404, detail="Monitor task not found")

    db.delete(monitor)
    db.commit()
    return {"message": "Monitor deleted"}
