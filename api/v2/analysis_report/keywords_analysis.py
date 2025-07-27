from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/keywords/wordcloud")
async def get_wordcloud():
    return [
        {"word": "ChatGPT", "size": 36},
        {"word": "Claude", "size": 28},
        {"word": "Gemini", "size": 24},
        {"word": "Llama", "size": 20},
        {"word": "AI chatbot", "size": 18},
        {"word": "openai", "size": 16},
        {"word": "huggingface", "size": 14},
        {"word": "anthropic", "size": 12},
        {"word": "large language model", "size": 10}
    ]


@router.get("/keywords/trend")
async def get_keyword_trend():
    return [
        {"date": "2025-07-21", "ChatGPT": 120, "Claude": 85, "Gemini": 60},
        {"date": "2025-07-22", "ChatGPT": 130, "Claude": 88, "Gemini": 70},
        {"date": "2025-07-23", "ChatGPT": 140, "Claude": 90, "Gemini": 75},
        {"date": "2025-07-24", "ChatGPT": 150, "Claude": 92, "Gemini": 78},
        {"date": "2025-07-25", "ChatGPT": 160, "Claude": 95, "Gemini": 80},
        {"date": "2025-07-26", "ChatGPT": 165, "Claude": 98, "Gemini": 82},
        {"date": "2025-07-27", "ChatGPT": 170, "Claude": 100, "Gemini": 85}
    ]


@router.get("/keywords/sentiment-ranking")
async def get_sentiment_ranking():
    return [
        {"keyword": "ChatGPT", "sentiment": "Positive", "score": 8.2},
        {"keyword": "Claude", "sentiment": "Positive", "score": 7.9},
        {"keyword": "Gemini", "sentiment": "Neutral", "score": 5.4},
        {"keyword": "Llama", "sentiment": "Neutral", "score": 5.7},
        {"keyword": "AI chatbot", "sentiment": "Negative", "score": 3.5},
        {"keyword": "anthropic", "sentiment": "Neutral", "score": 5.1},
        {"keyword": "huggingface", "sentiment": "Positive", "score": 7.0},
        {"keyword": "openai", "sentiment": "Positive", "score": 7.6},
        {"keyword": "large language model", "sentiment": "Neutral", "score": 5.9}
    ]


