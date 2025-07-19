from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 关联用户id，假设有 users 表
    query = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    results_count = Column(Integer, nullable=False)
    sentiment = Column(String(20))  # positive, negative, neutral
    platforms = Column(JSON)         # 存储平台列表
    analysis_result = Column(JSON)  # 存储分析结果JSON
    search_results = Column(JSON)   # 存储原始搜索结果JSON
