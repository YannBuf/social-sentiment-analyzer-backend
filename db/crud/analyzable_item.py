# backend/db/crud/analyzable_item.py

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AnalyzableItem
from db.models.AnalyzableItem import AnalyzableItemDBModel
from sqlalchemy import select
async def filter_existing_items(items: List[AnalyzableItem]) -> List[AnalyzableItem]:
    unique = []
    seen_urls = set()

    for item in items:
        if item.url in seen_urls:
            continue
        seen_urls.add(item.url)
        unique.append(item)

    return unique


async def save_items_to_db_if_not_exists(
    session: AsyncSession,
    items: List[AnalyzableItem]
) -> List[AnalyzableItem]:
    if not items:
        return []

    # 提取所有非空 URL
    urls = [item.url for item in items if item.url]

    # 查询 DB 中已有的 URL
    stmt = select(AnalyzableItemDBModel.url).where(AnalyzableItemDBModel.url.in_(urls))
    result = await session.execute(stmt)
    existing_urls = set(row[0] for row in result.fetchall())

    # 过滤出新项
    new_items = [item for item in items if item.url and item.url not in existing_urls]

    # 构造并入库
    for item in new_items:
        db_item = AnalyzableItemDBModel(
            platform=item.platform,
            content=item.content,
            author=item.author,
            publish_time=item.publish_time,
            url=item.url,
            likes=item.likes,
            comments=item.comments,
            shares=item.shares,
        )
        session.add(db_item)

    await session.commit()
    return new_items