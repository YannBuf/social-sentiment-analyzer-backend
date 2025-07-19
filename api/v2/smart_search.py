from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from api.services.crawler_controller import fetch_from_platforms  # 你的爬虫模块

router = APIRouter(tags=["Smart Search"])

# 请求与响应模型定义（保持不变）
class SearchRequest(BaseModel):
    query: str = Field(..., description="搜索关键词")
    platforms: List[str] = Field(..., description="平台列表")
    limit: Optional[int] = Field(50, description="最大返回条数")
    since: Optional[str] = Field(None, description="开始日期，格式YYYY-MM-DD")
    until: Optional[str] = Field(None, description="结束日期，格式YYYY-MM-DD")

class SearchResultItem(BaseModel):
    platform: str
    content: str
    author: str
    publish_time: datetime
    url: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None

class SearchResponse(BaseModel):
    results: List[SearchResultItem]
    totalCount: int

# 搜索接口，调用爬虫模块
@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        # 处理 since 参数，默认取过去7天
        if request.since:
            since_dt = datetime.strptime(request.since, "%Y-%m-%d")
        else:
            since_dt = datetime.utcnow() - timedelta(days=7)
        # 处理 until 参数，默认当前时间
        if request.until:
            until_dt = datetime.strptime(request.until, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
            # 加一天减一秒，保证直到23:59:59结束
        else:
            until_dt = datetime.utcnow()

        # 调用统一爬虫调度器抓取数据
        items = await fetch_from_platforms(
            query=request.query,
            platforms=request.platforms,
            total_limit=request.limit,
            since=since_dt,
            until=until_dt,
        )

        # 转换为响应格式
        results = []
        for item in items:
            results.append(SearchResultItem(
                platform=item.platform,
                content=item.content,
                author=item.author,
                publish_time=item.publish_time,
                likes=item.likes,
                comments=item.comments,
                shares=item.shares,
                url=item.url,
            ))

        return SearchResponse(results=results, totalCount=len(results))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")
