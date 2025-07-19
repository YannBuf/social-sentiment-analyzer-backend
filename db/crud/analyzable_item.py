# backend/db/crud/analyzable_item.py

from typing import List
from sqlalchemy.orm import Session
from db.models.AnalyzableItem import AnalyzableItemDBModel
from schemas import AnalyzableItem  # 你的数据模型

def filter_existing_items_sync(db: Session, items: List[AnalyzableItem]) -> List[AnalyzableItem]:
    urls = [item.url for item in items if item.url]
    existing = db.query(AnalyzableItemDBModel.url).filter(AnalyzableItemDBModel.url.in_(urls)).all()
    existing_urls = set(row[0] for row in existing)
    return [item for item in items if item.url and item.url not in existing_urls]

def save_items_to_db_if_not_exists_sync(db: Session, items: List[AnalyzableItem]) -> List[AnalyzableItem]:
    if not items:
        return []
    new_items = filter_existing_items_sync(db, items)
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
        db.add(db_item)
    db.commit()
    return new_items
