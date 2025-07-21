from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 创建SQLAlchemy引擎
# connect_args={"check_same_thread": False} 仅在SQLite时需要。
# 它允许多个线程（如FastAPI的请求）共享同一个连接。
engine = create_engine(
    settings.DATABASE_URL,connect_args={"check_same_thread":False}
)

# 创建一个SessionLocal类，每个实例都是 一个数据库会话
SessionLocal = sessionmaker(autoflush=False,bind=engine)

#创建一个Base类，我们的ORM模型将继承这个类
Base =declarative_base()
