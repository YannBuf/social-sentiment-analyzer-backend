"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import Settings
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()  # 会自动读取根目录的 .env 文件

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# URL encode 防止特殊字符导致错误
user = quote_plus(DB_USER)
password = quote_plus(DB_PASS)

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 用于 async FastAPI
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# 用于初始化脚本
sync_engine = create_engine(SYNC_DATABASE_URL)

SessionLocal = sessionmaker(bind=async_engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""