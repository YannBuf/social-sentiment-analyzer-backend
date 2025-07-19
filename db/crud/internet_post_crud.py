# db/crud/post_crud.py

from sqlalchemy.orm import Session
from db.models.data_unit import AnalyzableItem
from db.models.internet_post_model import PostItem
from datetime import datetime
import json

def save_items_to_db(items: list[AnalyzableItem], db: Session):
    for item in items:
        # 去重判断
        exists = db.query(PostItem).filter_by(link=item.link).first()
        if exists:
            continue

        post = PostItem(
            platform=item.platform,
            author=item.author,
            created_time=datetime.strptime(item.created_time, "%Y-%m-%d %H:%M:%S"),
            title=item.title,
            content=item.content,
            comments=json.dumps(item.comments, ensure_ascii=False),
            link=item.link,
        )
        db.add(post)

    db.commit()
