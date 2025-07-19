from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
import enum


class MonitorStatus(str, enum.Enum):
    processing = "processing"
    active = "active"
    paused = "paused"
    completed = "completed"


class MonitorTask(Base):
    __tablename__ = "monitor_tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    frequency = Column(String(50), nullable=True)
    keywords = Column(JSON)
    platforms = Column(JSON)
    status = Column(Enum(MonitorStatus), default=MonitorStatus.processing)
    sentiment = Column(JSON, default={"positive": 0, "neutral": 0, "negative": 0})
    mentions = Column(Integer, default=0)
    trend = Column(String(10), default="neutral")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="monitor_tasks")

    @property
    def lastUpdate(self):
        # 你可以返回真实的更新时间，比如 self.updated_at
        return "刚刚更新"
