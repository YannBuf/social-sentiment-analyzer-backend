from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/monitor/{monitor_id}/analysis")
async def get_monitor_analysis(monitor_id: str):
    return {
        "overview": {
            "totalMentions": 2722,
            "mentionChangePercent": 6.5,
            "sentimentScore": 6.8,
            "sentimentScoreChange": 0.2,
            "activeUsers": 1043,
            "activeUsersChangePercent": -1.8,
            "platformCount": 4,
            "platformLabel": "4 platforms"
        },
        "sentimentTrend": [
            {"date": "2025-07-21", "positive": 220, "neutral": 100, "negative": 80},
            {"date": "2025-07-22", "positive": 230, "neutral": 110, "negative": 70},
            {"date": "2025-07-23", "positive": 250, "neutral": 120, "negative": 80},
            {"date": "2025-07-24", "positive": 270, "neutral": 130, "negative": 70},
            {"date": "2025-07-25", "positive": 280, "neutral": 140, "negative": 60},
            {"date": "2025-07-26", "positive": 290, "neutral": 150, "negative": 50},
            {"date": "2025-07-27", "positive": 300, "neutral": 160, "negative": 40}
        ],
        "sentimentDistribution": {
            "positivePercent": 57,
            "neutralPercent": 23,
            "negativePercent": 20
        },
        "sentimentIntensity": [
            {"label": "Highly Positive", "value": 22},
            {"label": "Moderately Positive", "value": 35},
            {"label": "Neutral", "value": 23},
            {"label": "Moderately Negative", "value": 15},
            {"label": "Highly Negative", "value": 5}
        ],
        "trendAnalysis": [],
        "platformAnalysis": [],
        "keywordAnalysis": []
    }
