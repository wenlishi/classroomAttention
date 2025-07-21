from app.db import database,models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    logger.info("正在创建数据库表...")
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("数据库表创建成功！")

if __name__ == "__main__":
    init_database()
    