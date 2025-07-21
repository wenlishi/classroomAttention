import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print(project_root)
sys.path.insert(0, project_root)
from sqlalchemy import create_engine,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from sqlalchemy.exc import OperationalError 

# 创建SQLAlchemy引擎
# connect_args={"check_same_thread": False} 仅在SQLite时需要。
# 它允许多个线程（如FastAPI的请求）共享同一个连接。
# 准备连接参数
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

# 创建一个SessionLocal类，每个实例都是 一个数据库会话
SessionLocal = sessionmaker(autoflush=False,bind=engine)

#创建一个Base类，我们的ORM模型将继承这个类
Base =declarative_base()



if __name__=="__main__":
    # --- 新增的连接测试代码 ---
    print("正在尝试连接数据库...")
    
    try:
        # engine.connect() 会尝试建立一个真实的连接
        # 使用 'with' 语句可以确保连接在使用后被正确关闭
        with engine.connect() as connection:
            print("✅ 数据库连接成功！")
            # 可选：执行一个简单的查询来进一步验证
            result = connection.execute(text("SELECT 1"))
            print(f"✅ 简单查询成功，结果: {result.scalar_one()}")
            
    except OperationalError as e:
        print(f"❌ 数据库连接失败！")
        print(f"错误详情: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")