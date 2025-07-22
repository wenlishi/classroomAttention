from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import models
from app.schemas import user as user_schema
from app.schemas import session as session_schema
from app.core import security


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()


def create_user(db: Session, user: user_schema.UserCreate):
    """
    在数据库中创建一个新用户。
    - 接收 Pydantic schema 作为输入。
    - 处理密码哈希。
    - 创建 SQLAlchemy 模型实例并保存。
    """
    # 密码哈希的逻辑也属于“创建用户”这个业务的一部分，放在这里很合适
    hashed_password = security.get_password_hash(user.password)
     # 使用 Pydantic 的 model_dump() 方法更安全地转换数据
    user_data = user.model_dump(exclude={"password"})
    db_user = models.User(
        **user_data,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def create_class_session(db: Session, session: session_schema.SessionCreate, owner_id: str )->models.ClassSession:
    """在数据库中创建一条新的课堂会话记录"""
    session_data = session.model_dump()
    db_session = models.ClassSession(
        **session_data,
        owner_id=owner_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def create_analysis_task(db: Session, session_id: int, video_path: str)->models.AnalysisTask:
    """為离线分析模式创建一个任务记录"""
    db_task = models.AnalysisTask(
        session_id=session_id,
        video_path=video_path
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_sessions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """根据用户的id获取其创建的所有的课程会话"""
    return db.query(models.ClassSession).filter(models.ClassSession.owner_id == user_id).offset(skip).limit(limit).all()

def get_session(db: Session, session_id: int):
    """根据id获取单个课程会话"""
    return db.query(models.ClassSession).filter(models.ClassSession.id == session_id).first()

def get_user(db: Session, user_id: int) -> models.User | None:
    """
    根据用户ID从数据库中获取单个用户。
    """
    return db.query(models.User).filter(models.User.id == user_id).first()
 
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    """
    从数据库中获取一个用户列表，支持分页。
    """
    return db.query(models.User).offset(skip).limit(limit).all()
 
# 这是您已经有的函数，放在这里保持完整性
def update_user_is_active(db: Session, *, user: models.User, is_active: bool) -> models.User:
    """更新指定用户的 is_active 状态"""
    user.is_active = is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user