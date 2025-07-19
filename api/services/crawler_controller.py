from typing import List
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from api.adapters.reddit_adapter import RedditAdapter
from api.adapters.Base_Adapter import BasePlatformAdapter
from db.models.data_unit import AnalyzableItem
from db.database import SessionLocal  # 同步Session
from db.crud.analyzable_item import save_items_to_db_if_not_exists_sync

# 平台适配器注册
PLATFORM_ADAPTERS: dict[str, BasePlatformAdapter] = {
    "reddit": RedditAdapter(),
    # 后续添加更多平台...
}

executor = ThreadPoolExecutor(max_workers=5)


async def save_items_async(items: List[AnalyzableItem]) -> List[AnalyzableItem]:
    loop = asyncio.get_running_loop()

    def db_task():
        with SessionLocal() as db:
            return save_items_to_db_if_not_exists_sync(db, items)

    new_items = await loop.run_in_executor(executor, db_task)
    return new_items


async def fetch_from_platforms(
    query: str,
    platforms: List[str],
    total_limit: int,
    since: datetime,
    until: datetime | None = None
) -> List[AnalyzableItem]:
    results: List[AnalyzableItem] = []
    per_platform_limit = max(total_limit // len(platforms), 1)

    for platform in platforms:
        adapter = PLATFORM_ADAPTERS.get(platform)
        if not adapter:
            continue

        try:
            # 异步调用爬虫采集数据
            fetched = await adapter.fetch(query=query, limit=per_platform_limit, since=since, until=until)

            # 异步调用同步写库函数，写入数据库并去重
            truly_new = await save_items_async(fetched)

            results.extend(truly_new)

        except Exception as e:
            print(f"❌ Error fetching from {platform}: {e}")

    return results
