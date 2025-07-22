from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import models
from app.schemas import user as user_schema
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

