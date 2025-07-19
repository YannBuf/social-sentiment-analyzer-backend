# backend/services/crawler_controller.py

from typing import List
from datetime import datetime
from db.database import AsyncSessionLocal

from api.adapters.reddit_adapter import RedditAdapter
from api.adapters.Base_Adapter import BasePlatformAdapter
from db.models.data_unit import AnalyzableItem
from db.crud.analyzable_item import save_items_to_db_if_not_exists, filter_existing_items

# 平台适配器注册
PLATFORM_ADAPTERS: dict[str, BasePlatformAdapter] = {
    "reddit": RedditAdapter(),
    # 后续添加更多平台...
}


async def fetch_from_platforms(
    query: str,
    platforms: List[str],
    total_limit: int,
    since: datetime,
    until: datetime | None = None
) -> List[AnalyzableItem]:
    results: List[AnalyzableItem] = []
    per_platform_limit = max(total_limit // len(platforms), 1)

    async with AsyncSessionLocal() as session:
        for platform in platforms:
            adapter = PLATFORM_ADAPTERS.get(platform)
            if not adapter:
                continue

            try:
                fetched = await adapter.fetch(query=query, limit=per_platform_limit, since=since, until=until)

                # 去重处理：从 DB 中查已有的链接/哈希，排除重复（你可以也传 session 给 filter_existing_items）
                new_items = await filter_existing_items(fetched)

                # 批量入库
                truly_new = await save_items_to_db_if_not_exists(session, new_items)

                results.extend(truly_new)

            except Exception as e:
                print(f"❌ Error fetching from {platform}: {e}")

    return results
