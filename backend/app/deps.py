from app.db.database import SessionLocal

def get_db():
    """
    FastAPI 依赖项，用于获取数据库会话。
    它会为每个请求创建一个新的会话，并在请求结束后关闭它。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_active_user():
    pass