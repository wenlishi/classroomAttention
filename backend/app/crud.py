from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload # 用于优化查询
from fastapi import Depends
from typing import Optional
from app.db import models
from app.schemas import user as user_schema
from app.schemas import session as session_schema
from app.schemas import layout as layout_schema
from app.core import security


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

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
    db_session = models.ClassSession(
        session_name=session.session_name,
        session_type=session.session_type,  # <--- 最关键的修改！提取枚举的值 'offline'
        # session_status 和 start_time 会由 model 的 default 值自动处理
        # 如果你的 Pydantic schema 中也定义了 start_time，可以像下面一样加上
        # start_time=session.start_time, 
        owner_id=owner_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete_session(db: Session, *, db_obj: models.ClassSession) -> models.ClassSession:
    db.delete(db_obj)
    db.commit()
    return db_obj

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




# --- Layout and Desk CRUD ---
def get_layout(db: Session, layout_id: int) -> models.ClassroomLayerout | None:
    """获取单个布局及其所有桌子 (使用 joinedload 优化)"""
    return (
        db.query(models.ClassroomLayout)
        .options(joinedload(models.ClassroomLayout.desks)) # 关键优化: 一次性加载关联的桌子
        .filter(models.ClassroomLayout.id == layout_id)
        .first()
    )

def get_layouts_by_owner(db: Session, *, owner_id: int, skip: int = 0, limit: int = 100)-> List[models.ClassroomLayout]:
    """根据所有者ID获取其创建的所有布局列表 (不含桌子详情，仅列表)"""
    return (
        db.query(models.ClassroomLayout)
        .filter(models.ClassroomLayout.owner_id)
        .order_by(models.ClassroomLayout.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_layout_with_desks(db: Session, *, layout_in: layout_schema.ClassroomLayoutCreate, owner_id: int, image_url: Optional[str] = None)-> models.ClassroomLayout:
    """为指定用户创建一个包含多张桌子的新布局"""
    # 1. 创建布局主体
    layout_data = layout_in.models_dump(exclude={"desks"})
    db_layout = models.ClassroomLayout(**layout_data, owner_id=owner_id)
    # ↓↓↓ 将图片URL也加入到创建数据中 ↓↓↓
    db_layout = models.ClassroomLayout(**layout_data, owner_id=owner_id, background_image_url=image_url)
    db.add(db_layout)
    db.commit() # 提交以获取 db_layout.id
    db.refresh(db_layout)
 
    # 2. 批量创建桌子并关联到新布局
    desks_data = layout_in.model_dump()["desks"]
    db_desks = []
    for desk_data in desks_data:
        db_desk = models.Desk(**desk_data, layout_id=db_layout.id)
        db_desks.append(db_desk)
    
    db.add_all(db_desks)
    db.commit()
    db.refresh(db_layout)

    return db_layout

def delete_layout(db: Session, *, db_obj: models.ClassroomLayout) -> models.ClassroomLayout:
    """从数据库删除一个布局 (关联的桌子也会被自动删除)"""
    db.delete(db_obj)
    db.commit()
    return db_obj



