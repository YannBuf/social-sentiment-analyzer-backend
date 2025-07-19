""""
废弃的function
"""
from fastapi import APIRouter, BackgroundTasks
from db.models.monitor_model import MonitorCreateRequest, MonitorStatus
from typing import Dict
import random
import time

router = APIRouter()

# 简单的内存存储模拟
monitor_tasks: Dict[int, MonitorStatus] = {}

def simulate_analysis(task_id: int):
    # 模拟耗时
    time.sleep(5)  # 假设5秒分析完成
    sentiment = {
        "positive": random.randint(20, 60),
        "neutral": random.randint(10, 30),
    }
    sentiment["negative"] = 100 - sentiment["positive"] - sentiment["neutral"]

    mentions = random.randint(100, 2000)
    trend = "up" if random.random() > 0.5 else "down"

    # 更新任务
    monitor = monitor_tasks[task_id]
    monitor.status = "completed"
    monitor.sentiment = sentiment
    monitor.mentions = mentions
    monitor.trend = trend
    monitor.last_update = "刚刚"
    monitor_tasks[task_id] = monitor


@router.post("/monitor/create")
def create_monitor(data: MonitorCreateRequest, background_tasks: BackgroundTasks):
    task_id = int(time.time() * 1000)  # 毫秒时间戳当作ID

    # 先存为分析中的状态
    monitor = MonitorStatus(
        id=task_id,
        name=data.name,
        status="processing"
    )
    monitor_tasks[task_id] = monitor

    # 异步后台模拟分析
    background_tasks.add_task(simulate_analysis, task_id)

    return {"task_id": task_id}


@router.get("/monitor/{task_id}/status")
def get_monitor_status(task_id: int):
    """
    monitor = monitor_tasks.get(task_id)
    if not monitor:
        return {"error": "Monitor task not found"}
    return monitor
    """
    return {
        "monitor_id": task_id,
        "status": "completed",
        "sentiment": {"positive": 60, "neutral": 30, "negative": 10},
        "mentions": 1234,
        "trend": "up"
    }