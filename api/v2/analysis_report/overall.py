from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/monitor/{monitor_id}/analysis")
async def get_monitor_analysis(monitor_id: str):
    # 这里可以根据 monitor_id 查询数据库或模拟数据
    #if monitor_id != "demo123":
    #    raise HTTPException(status_code=404, detail="Monitor not found")

    return {
        "overview": {
            "totalMentions": 24567,
            "mentionChangePercent": 15.3,
            "sentimentScore": 7.2,
            "sentimentScoreChange": 0.3,
            "activeUsers": 8924,
            "activeUsersChangePercent": -2.1,
            "platformCount": 8,
            "platformLabel": "全平台"
        },
        "sentimentTrend": [
            {"date": "2025-06-25", "positive": 120, "neutral": 80, "negative": 40},
            {"date": "2025-06-26", "positive": 150, "neutral": 90, "negative": 60},
            {"date": "2025-06-27", "positive": 170, "neutral": 100, "negative": 70},
            {"date": "2025-06-28", "positive": 160, "neutral": 110, "negative": 80},
            {"date": "2025-06-29", "positive": 180, "neutral": 120, "negative": 60},
            {"date": "2025-06-30", "positive": 190, "neutral": 130, "negative": 50},
            {"date": "2025-07-01", "positive": 200, "neutral": 140, "negative": 40}
        ],
        "sentimentDistribution": {
            "positivePercent": 68,
            "neutralPercent": 22,
            "negativePercent": 10
        },
        "sentimentIntensity": [
            {"label": "极度正面", "value": 25},
            {"label": "中度正面", "value": 45},
            {"label": "中性", "value": 20},
            {"label": "中度负面", "value": 8},
            {"label": "极度负面", "value": 2}
        ],
        "trendAnalysis": [],
        "platformAnalysis": [],
        "keywordAnalysis": []
    }