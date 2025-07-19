from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import Settings

# Connect to database
ASYNC_DATABASE_URL = f"mysql+aiomysql://{Settings.DB_USER}:{Settings.DB_PASS}@{Settings.DB_HOST}/{Settings.DB_NAME}"
SYNC_DATABASE_URL = f"mysql+mysqlconnector://{Settings.DB_USER}:{Settings.DB_PASS}@{Settings.DB_HOST}/{Settings.DB_NAME}"

# 用于 async FastAPI
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# 用于初始化脚本
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(bind=sync_engine)



Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

