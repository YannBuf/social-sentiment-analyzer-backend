# api/routes/analyze.py

import os
import json
import openai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Union, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

# 请求体模型
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze, English only")

# 响应模型
class AnalyzeResponse(BaseModel):
    sentiment: str
    confidence: int
    emotions: Dict[str, float]
    keywords: List[str]

# 通用调用OpenAI接口函数
async def call_openai_chat(
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.5,
        system_prompt: str = None,
) -> Union[Dict[str, Any], str]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        result_text = response.choices[0].message.content.strip()

        print("OpenAI raw response:", repr(result_text))  # 方便调试

        # 预处理：去除可能存在的 markdown 格式（```json ... ```）
        if result_text.startswith("```"):
            # 取中间内容
            lines = result_text.split("\n")
            if len(lines) >= 3:
                result_text = "\n".join(lines[1:-1]).strip()

        try:
            return json.loads(result_text)
        except json.JSONDecodeError as e:
            # 返回详细错误，方便前端定位问题
            return {"error": f"JSON decode error: {str(e)}", "raw_response": result_text}

    except Exception as e:
        return {"error": str(e)}


# 分析文本的Prompt模板（注意这里是一个完整字符串，{input_text}在里面）
ANALYSIS_PROMPT_TEMPLATE = """
You are an advanced English sentiment analysis AI.

Please analyze the following English text with these instructions:

1. Determine the overall sentiment: "positive", "negative", or "neutral".

2. Provide a confidence score for this overall sentiment, expressed as a percentage from 0% to 100%.
   - For example, if the sentiment is "negative", the confidence indicates how strongly negative it is.

3. Based on the overall sentiment detected, break down the emotions into relevant categories with scores between 0 and 1 (0 means absence, 1 means very strong presence):

   - If the overall sentiment is "positive", provide scores for these emotions: joy, trust, anticipation, surprise.
   - If the overall sentiment is "negative", provide scores for these emotions: anger, sadness, fear, disgust.
   - If the overall sentiment is "neutral", provide scores for these emotions: calmness, acceptance, boredom, neutrality.

   Only include the emotion categories relevant to the overall sentiment in your response.

4. Extract up to 5 key keywords or key phrases that best summarize the content.

Please return the result strictly in the following JSON format:

{{
  "sentiment": "positive / negative / neutral",
  "confidence": 0,
  "emotions": {{
    // only the relevant categories as explained above, each score 0.0 - 1.0
  }},
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Here is the text to analyze:

\"\"\"
{input_text}
\"\"\"
"""

# 分析函数，调用OpenAI接口
async def analyze_english_text(input_text: str) -> Union[Dict[str, Any], str]:
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(input_text=input_text)
    system_prompt = "You are a helpful and accurate English sentiment analysis assistant."
    result = await call_openai_chat(prompt=prompt, system_prompt=system_prompt, temperature=0.4)
    return result

# FastAPI接口路由
@router.post("/sentence_analyze", response_model=Union[AnalyzeResponse, Dict[str, str]])
async def analyze_endpoint(request: AnalyzeRequest):
    result = await analyze_english_text(request.text)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    try:
        return AnalyzeResponse(
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            emotions=result["emotions"],
            keywords=result["keywords"],
        )
    except (KeyError, TypeError):
        raise HTTPException(status_code=500, detail="Invalid response format from analysis service")
