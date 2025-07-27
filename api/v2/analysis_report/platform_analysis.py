from fastapi import APIRouter, HTTPException

router = APIRouter()

platform_mentions = [
    {"platform": "X", "mentions": 1100},
    {"platform": "Reddit", "mentions": 850},
    {"platform": "YouTube", "mentions": 500},
    {"platform": "Facebook", "mentions": 272}
]


platform_sentiments = {
    "X": [
        {"name": "Positive", "value": 650},
        {"name": "Neutral", "value": 300},
        {"name": "Negative", "value": 150},
    ],
    "Reddit": [
        {"name": "Positive", "value": 470},
        {"name": "Neutral", "value": 230},
        {"name": "Negative", "value": 150},
    ],
    "YouTube": [
        {"name": "Positive", "value": 310},
        {"name": "Neutral", "value": 110},
        {"name": "Negative", "value": 80},
    ],
    "Facebook": [
        {"name": "Positive", "value": 130},
        {"name": "Neutral", "value": 60},
        {"name": "Negative", "value": 82},
    ]
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
