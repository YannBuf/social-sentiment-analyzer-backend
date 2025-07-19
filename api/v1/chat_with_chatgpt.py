from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from core.config import Settings

# 初始化 OpenAI 客户端
client = OpenAI(api_key=Settings.OPENAI_API_KEY)

# 创建 Router 实例
router = APIRouter()

# 定义请求体
class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"  # 默认模型

# 创建 chat 接口
@router.post("/chat")
async def chat_with_chatgpt(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
