# db/models/post_model.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PostItem(Base):
    __tablename__ = "internet_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(20), default="reddit")
    author = Column(String(100))
    created_time = Column(DateTime)
    title = Column(String(300))
    content = Column(Text)
    comments = Column(Text)  # 以 JSON 字符串保存 comment 列表
    link = Column(String(500), unique=True)  # 去重依据
    inserted_at = Column(DateTime, default=datetime.utcnow)
