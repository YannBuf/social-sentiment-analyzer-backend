from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from datetime import datetime
import json

# 假设你已经有这个通用调用OpenAI的异步函数
from api.v2.sentence_sentiment_analysis import call_openai_chat

router = APIRouter(tags=["Smart search"])


class SearchResultItem(BaseModel):
    id: str
    platform: str
    content: str
    author: str
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    url: Optional[str] = None
    publishTime: datetime
    @model_validator(mode='before')
    def parse_publish_time(cls, values):
        pt = values.get('publishTime')
        if isinstance(pt, str):
            pt = pt.replace('/', '-')
            # 也可以用 datetime.strptime(pt, '%Y-%m-%d %H:%M') 转成 datetime
        values['publishTime'] = pt
        return values



class AnalyzeRequest(BaseModel):
    query: str
    platforms: List[str]
    searchResults: List[SearchResultItem]


class OverallSentiment(BaseModel):
    label: str
    confidence: float
    score: float


class AnalysisResult(BaseModel):
    overall_sentiment: OverallSentiment
    emotions: dict
    keywords: List[str]
    topics: List[str]
    summary: str
    insights: List[str]
    recommendations: List[str]


# Prompt模板：让OpenAI给出综合分析
ANALYZE_PROMPT_TEMPLATE = """
You are an advanced AI analyst specialized in social media sentiment and topic analysis.

Given the following social media posts related to the keyword "{query}", please analyze and provide the following in JSON format:

1. overall_sentiment: label ("positive", "neutral", or "negative"), confidence (0.0-1.0), and score (sentiment intensity).
2. emotions: a dictionary of emotions relevant to the sentiment.
3. keywords: up to 10 key keywords or phrases summarizing the content.
4. topics: a list of main topics discussed.
5. summary: a concise summary of the overall public opinion.
6. insights: 3-5 key insights based on the posts.
7. recommendations: 3-5 actionable recommendations.

Here are the posts:

{posts}

Return strictly a JSON object with the keys above.
"""


@router.post("/smart_search_analyze", response_model=AnalysisResult)
async def analyze(request: AnalyzeRequest):
    # 拼接搜索结果内容，格式化为 "[平台] 作者: 内容" 形式，方便模型理解
    posts_text = "\n\n".join(
        f"[{item.platform}] {item.author}: {item.content}"
        for item in request.searchResults
    )

    prompt = ANALYZE_PROMPT_TEMPLATE.format(query=request.query, posts=posts_text)

    try:
        result = await call_openai_chat(
            prompt=prompt,
            system_prompt="You are a helpful and accurate AI analyst.",
            temperature=0.4,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # 验证并转换返回数据
    try:
        return AnalysisResult(
            overall_sentiment=OverallSentiment(**result["overall_sentiment"]),
            emotions=result["emotions"],
            keywords=result["keywords"],
            topics=result["topics"],
            summary=result["summary"],
            insights=result["insights"],
            recommendations=result["recommendations"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid response format: {str(e)}")
