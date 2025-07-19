# main.py
from db.database import engine
from db.models.dashboard_model import Base

def create_database():
    print("开始创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")

if __name__ == "__main__":
    create_database()
