# backend/openai_analyzer.py

import os
import openai
import json
from pydantic import BaseModel
from typing import Literal

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class AnalyzeRequest(BaseModel):
    keyword: str
    product: Literal["Top", "Latest", "Media"] = "Latest"
    max_count: int = 20

async def analyze_tweets_text(tweets_text: str) -> dict:
    prompt = f"""
You are a social media analyst. Please analyze the overall sentiment and topics in the following social media content:
{tweets_text}

Return the result in the following JSON format:

{{
  "sentiment": "positive / negative / neutral",
  "summary": "brief summary of the public opinion",
  "keywords": ["keyword1", "keyword2", "..."]
}}
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        result_text = response.choices[0].message.content.strip()
        return json.loads(result_text)
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze_sentiment(data: AnalyzeRequest):
    tweets = await fetch_tweets_async(data.keyword, product=data.product, max_count=data.max_count)
    tweets_text = "\n\n".join([f"{t['user']}: {t['text']}" for t in tweets])
    result = await analyze_tweets_text(tweets_text)
    return {
        "keyword": data.keyword,
        "tweet_count": len(tweets),
        "analysis": result
    }