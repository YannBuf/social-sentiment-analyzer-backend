from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/keywords/wordcloud")
async def get_wordcloud():
    return [
        {"word": "新品发布会", "size": 28},
        {"word": "用户体验", "size": 24},
        {"word": "客服", "size": 20},
        {"word": "功能更新", "size": 18},
        {"word": "响应时间", "size": 16},
        {"word": "界面设计", "size": 14},
        {"word": "稳定性", "size": 12},
        {"word": "优惠活动", "size": 10},
        {"word": "WIFI", "size": 100}

    ]

@router.get("/keywords/trend")
async def get_keyword_trend():
    return [
        {"date": "2025-06-25", "新品发布会": 120, "功能更新": 100, "客服": 80},
        {"date": "2025-06-26", "新品发布会": 140, "功能更新": 110, "客服": 90},
        {"date": "2025-06-27", "新品发布会": 160, "功能更新": 120, "客服": 85},
        {"date": "2025-06-28", "新品发布会": 180, "功能更新": 130, "客服": 70},
        {"date": "2025-06-29", "新品发布会": 200, "功能更新": 150, "客服": 60},
        {"date": "2025-06-30", "新品发布会": 220, "功能更新": 160, "客服": 50},
        {"date": "2025-07-01", "新品发布会": 250, "功能更新": 180, "客服": 40},
    ]

@router.get("/keywords/sentiment-ranking")
async def get_sentiment_ranking():
    return [
        {"keyword": "新品发布会", "sentiment": "正面", "score": 8.5},
        {"keyword": "功能更新", "sentiment": "正面", "score": 7.9},
        {"keyword": "客服", "sentiment": "负面", "score": 3.2},
        {"keyword": "响应时间", "sentiment": "负面", "score": 4.1},
        {"keyword": "用户体验", "sentiment": "中性", "score": 5.5},
    ]
