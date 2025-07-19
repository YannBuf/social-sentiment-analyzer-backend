from fastapi import APIRouter, BackgroundTasks
from db.models.monitor_model import MonitorCreateRequest, MonitorStatus
from typing import Dict
import random
import time

router = APIRouter()



@router.get("/sentiment/trend")
async def get_sentiment_trend():
    data = [
        {"date": "2025-06-25", "positive": 120, "neutral": 80, "negative": 40},
        {"date": "2025-06-26", "positive": 150, "neutral": 90, "negative": 60},
        {"date": "2025-06-27", "positive": 170, "neutral": 100, "negative": 70},
        {"date": "2025-06-28", "positive": 160, "neutral": 110, "negative": 80},
        {"date": "2025-06-29", "positive": 180, "neutral": 120, "negative": 60},
        {"date": "2025-06-30", "positive": 190, "neutral": 130, "negative": 50},
        {"date": "2025-07-01", "positive": 200, "neutral": 140, "negative": 40},
    ]
    return data

@router.get("/sentiment/intensity")
async def get_sentiment_intensity():
    data = [
        {"label": "极度正面", "value": 25},
        {"label": "中度正面", "value": 45},
        {"label": "中性", "value": 20},
        {"label": "中度负面", "value": 8},
        {"label": "极度负面", "value": 2},
    ]
    return data