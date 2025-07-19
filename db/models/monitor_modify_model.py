from sqlalchemy import Column, Integer, String, JSON
from db.database import Base
class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    frequency = Column(String, default="realtime")
    keywords = Column(JSON, default=[])
    platforms = Column(JSON, default=[])
