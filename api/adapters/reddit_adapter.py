# backend/adapters/reddit_adapter.py

import asyncpraw
import asyncio
from datetime import datetime
from typing import List
from db.models.data_unit import AnalyzableItem
from api.adapters.Base_Adapter import BasePlatformAdapter  # 你定义的抽象基类
from dotenv import load_dotenv
import os

# 加载根目录或当前目录下的 .env 文件
load_dotenv()

class RedditAdapter(BasePlatformAdapter):
    def __init__(self):
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent = os.getenv("USER_AGENT")

        if not client_id or not client_secret or not user_agent:
            raise ValueError("Reddit API credentials not set in environment variables")

        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    async def fetch(self, query: str, limit: int, since: datetime, until: datetime | None = None, include_comments: bool = True) -> List[AnalyzableItem]:
        subreddit = await self.reddit.subreddit("all")
        submissions = subreddit.search(query, sort="relevance", limit=limit)

        tasks = []
        async for submission in submissions:
            created = datetime.fromtimestamp(submission.created_utc)
            if created < since:
                continue
            if until and created > until:
                continue
            if submission.score < 3:
                continue
            if submission.is_self and len(submission.selftext or "") < 50:
                continue
            if "[removed]" in (submission.selftext or "").lower():
                continue

            tasks.append(fetch_post_details(submission, include_comments))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        items = [res for res in results if isinstance(res, AnalyzableItem)]
        return items

async def fetch_post_details(submission, include_comments: bool = False) -> AnalyzableItem:
    try:
        await submission.load()

        content = ""
        if submission.is_self:
            content = submission.selftext.strip()
        else:
            content = submission.title.strip()
        if len(content) < 30:
            return None

        """
        content = (
            submission.selftext.strip()
            if submission.selftext
            else f"[🔗 External link] {submission.url}"
        )"""

        comments_count = 0
        if include_comments:
            try:
                await submission.comments.replace_more(limit=0)
                top_comments = submission.comments[:3]
                comments = []
                for comment in top_comments:
                    body = comment.body.strip()
                    # 简单排除只有链接的评论（比如只包含"http"）
                    if len(body) >= 10 and "http" not in body.lower():
                        comments.append(body[:200].replace('\n', ' '))
                comments_count = len(comments)
            except Exception:
                comments_count = 0

        return AnalyzableItem(
            platform="reddit",
            author=str(submission.author),
            publish_time=datetime.fromtimestamp(submission.created_utc),
            content=content[:1000],
            url=f"https://reddit.com{submission.permalink}",
            likes=submission.score,
            comments=comments_count,
            shares=0,
        )
    except Exception as e:
        # 可以加日志：print(f"Error fetching post: {e}")
        return None
