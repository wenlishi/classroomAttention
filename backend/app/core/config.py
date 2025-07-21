import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
     # 数据库URL
    # 对于SQLite, 格式是 "sqlite:///./your_database_name.db"
    # 这个路径是相对于你运行uvicorn的根目录（即 backend/）
    DATABASE_URL: str = "sqlite:///./test.db"
 
    # JWT 配置
    # !!! 警告: 这是一个极其重要的安全密钥 !!!
    # !!! 在生产环境中，绝不要硬编码这个值，要通过环境变量加载 !!!
    # 可以用这个命令生成一个新的密钥: openssl rand -hex 32
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token有效期为30分钟

    class Config():
        case_senstive = True


# 创建一个全局可用的配置实例
settings = Settings()
