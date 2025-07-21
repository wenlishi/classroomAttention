import secrets
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
     # 数据库URL
    # 对于SQLite, 格式是 "sqlite:///./your_database_name.db"
    # 这个路径是相对于你运行uvicorn的根目录（即 backend/）
    DATABASE_URL: str 
 
    # JWT 配置
    # !!! 警告: 这是一个极其重要的安全密钥 !!!
    # !!! 在生产环境中，绝不要硬编码这个值，要通过环境变量加载 !!!
    # 可以用这个命令生成一个新的密钥: openssl rand -hex 32
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    class Config():
        case_sensitive = True #大小写敏感
        env_file = ".env"


# 创建一个全局可用的配置实例
settings = Settings()

