from fastapi import APIRouter, BackgroundTasks
from db.models.monitor_model import MonitorCreateRequest, MonitorStatus
from typing import Dict
import random
import time

router = APIRouter()



@router.get("/sentiment/trend")
async def get_sentiment_trend():
    data = [
        {"date": "2025-07-21", "positive": 220, "neutral": 100, "negative": 80},
        {"date": "2025-07-22", "positive": 230, "neutral": 110, "negative": 70},
        {"date": "2025-07-23", "positive": 250, "neutral": 120, "negative": 80},
        {"date": "2025-07-24", "positive": 270, "neutral": 130, "negative": 70},
        {"date": "2025-07-25", "positive": 280, "neutral": 140, "negative": 60},
        {"date": "2025-07-26", "positive": 290, "neutral": 150, "negative": 50},
        {"date": "2025-07-27", "positive": 300, "neutral": 160, "negative": 40},
    ]
    return data


@router.get("/sentiment/intensity")
async def get_sentiment_intensity():
    data = [
        {"label": "Strongly Positive", "value": 25},
        {"label": "Moderately Positive", "value": 45},
        {"label": "Neutral", "value": 20},
        {"label": "Moderately Negative", "value": 8},
        {"label": "Strongly Negative", "value": 2},
    ]
    return data
