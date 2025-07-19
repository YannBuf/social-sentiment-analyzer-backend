from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import asyncpraw
from datetime import datetime
import asyncio
from core.config import Settings
from typing import List

router = APIRouter()

# 🧠 异步获取帖子的详情并返回 dict 而不是打印
async def fetch_post_details(submission):
    await submission.load()
    created_time = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
    content = submission.selftext.strip() if submission.selftext else f"[🔗 外部链接] {submission.url}"

    post = {
        "title": submission.title,
        "author": str(submission.author),
        "created_time": created_time,
        "score": submission.score,
        "num_comments": submission.num_comments,
        "link": f"https://reddit.com{submission.permalink}",
        "content": content[:500],
        "top_comments": []
    }

    try:
        await submission.comments.replace_more(limit=0)
        top_comments = submission.comments[:3]
        post["top_comments"] = [
            comment.body[:200].replace('\n', ' ') for comment in top_comments
        ]
    except Exception as e:
        post["top_comments"] = [f"⚠️ 获取评论失败: {e}"]

    return post

# 🔍 Reddit 搜索协程
async def search_reddit(query: str):
    reddit = asyncpraw.Reddit(
        client_id=Settings.CLIENT_ID,
        client_secret=Settings.CLIENT_SECRET,
        user_agent=Settings.USER_AGENT
    )

    subreddit = await reddit.subreddit("all")
    submissions = subreddit.search(query, sort="relevance", limit=20)

    tasks = []
    async for submission in submissions:
        if submission.score < 3:
            continue
        if submission.is_self and len(submission.selftext) < 50:
            continue
        if "[removed]" in submission.selftext.lower():
            continue
        tasks.append(fetch_post_details(submission))

    results = await asyncio.gather(*tasks)
    await reddit.close()
    return results

# 🌐 FastAPI 路由
@router.get("/search_reddit")
async def search(query: str = Query(..., description="搜索关键词")):
    try:
        results = await search_reddit(query)
        return JSONResponse(content={"query": query, "results": results})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
