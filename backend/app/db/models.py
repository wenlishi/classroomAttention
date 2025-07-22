import datetime
from sqlalchemy import (Integer, 
                        String,
                        Column,
                        DateTime,
                        Float,
                        ForeignKey,
                        Enum as SQLAlchemyEnum,)
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False, default="teacher")
    created_at = Column(DateTime, default=datetime.datetime.now())
    #关系： 一个用户（教师）可以创建多个课堂会话
    sessions = relationship("ClassSession", back_populates="owner")


class ClassSession(Base):
    """
    课堂会话表，定义一次教学活动（一节课），是所有分析的“容器”。
    可以是一次离线视频分析，也可以是一次实时监控。
    """

    __tablename__ = "class_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, index=True, nullable=False)
    session_type = Column(SQLAlchemyEnum("offline", "realtime", name="session_type_enum"), nullable=False)
    session_status = Column(SQLAlchemyEnum("pending", "processing", "completed", "failed", name="session_status_enum"), nullable=False, default="pending")
    start_time = Column(DateTime, default=datetime.datetime.now())
    end_time = Column(DateTime, nullable=True)

    #外键，关联到创建者（用户）
    owner_id = Column(Integer, ForeignKey("users.id"))

    #关系
    owner = relationship("User", back_populates="sessions")
    task = relationship("AnalysisTask", back_populates="session", uselist=False)
    logs = relationship("AttentionLog", back_populates="session")
    reports = relationship("AttentionReport", back_populates="session")

class AnalysisTask(Base):
    """（离线模式专用）分析任务表，跟踪视频上传和处理的状态"""
    __tablename__ = "analysis_tasks"

    id = Column(Integer, primary_key= True, index=True)
    video_path = Column(String, nullable=False)
    celery_task_id = Column(String, nullable=True, index=True)
    
    #外键 ： 与课堂会话是一对一的关系
    session_id = Column(Integer, ForeignKey("class_sessions.id"), unique=True, nullable=False)
    # 关系
    session = relationship("ClassSession", back_populates="task")

# ------------- 数据结果模型 (简化版) -------------
class AttentionLog(Base):
    """
    原始数据记录表。
    存储在一次会话中，某个被追踪到的匿名个体的详细状态。
    """
    __tablename__ = "attention_logs"
    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(Float, nullable=False) # 视频中的秒数或实时会话的时间戳
    attention_status = Column(SQLAlchemyEnum("head_up","head_down", name="attention_status_enum"), nullable=False)
    
    # 外键： 关联是哪一次的会话
    session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    
    session = relationship("ClassSession", back_populates="logs")

class AttentionReport(Base):
    """
    分析报告/摘要表。
    存储对一次会话中，某个被追踪到的匿名个体的最终量化分析结果。
    """
    __tablename__ = "attention_reports"

    id = Column(Integer, primary_key=True, index=True)

    attention_score = Column(Float, nullable=False)
    total_duration = Column(Float, nullable=False)
    report_generated_at = Column(DateTime, default=datetime.datetime.now())

    # 外键： 关联到是哪一次的会话
    session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)

    session = relationship("ClassSession", back_populates="reports")
