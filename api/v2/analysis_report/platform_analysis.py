from fastapi import APIRouter, HTTPException

router = APIRouter()

platform_mentions = [
    {"platform": "Twitter", "mentions": 12000},
    {"platform": "Facebook", "mentions": 15000},
    {"platform": "Instagram", "mentions": 9000},
    {"platform": "Weibo", "mentions": 7000},
    {"platform": "LinkedIn", "mentions": 3000},
]

platform_sentiments = {
    "Twitter": [
        {"name": "正面", "value": 4000},
        {"name": "中性", "value": 6000},
        {"name": "负面", "value": 2000},
    ],
    "Facebook": [
        {"name": "正面", "value": 3000},
        {"name": "中性", "value": 8000},
        {"name": "负面", "value": 4000},
    ],
    # 你可以继续补充
}

@router.get("/platforms/mentions")
async def get_platform_mentions():
    return platform_mentions

@router.get("/platforms/{platform_name}/sentiment")
async def get_platform_sentiment(platform_name: str):
    sentiment = platform_sentiments.get(platform_name)
    if sentiment is None:
        raise HTTPException(status_code=404, detail="平台未找到或无情感数据")
    return sentiment
