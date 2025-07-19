from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AnalyzableItemDBModel(Base):
    __tablename__ = "analyzable_items"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 数据库自动生成主键
    platform = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=True)
    publish_time = Column(DateTime, nullable=False)
    url = Column(String(500), nullable=True)
    likes = Column(Integer, nullable=True, default=0)
    comments = Column(Integer, nullable=True, default=0)
    shares = Column(Integer, nullable=True, default=0)

    def __repr__(self):
        return f"<AnalyzableItem(id={self.id}, platform={self.platform})>"
