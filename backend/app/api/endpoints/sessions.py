# 课程会话，就是课程的记录

import datetime
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud,deps
from app.db import models
from app.schemas import session as session_schema
from app.db.models import SessionType

router = APIRouter()

#定义视频上传的存储目录
VIDEO_STORAGE_PATH = Path("medio/videos")
VIDEO_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=session_schema.SessionCreate)
def create_session_with_video_upload(
    *,
    db: Session = Depends(deps.get_db),
    # 注意：我们同时接收文件和表单数据
    session_name: str = Form(...),
    video_file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_user) #  关键：保护此端点
):
    """
    创建一个新的离线分析会话，并上传视频。
    - 需要用户认证。
    - 接收一个视频文件和一个会话名称。
    """
    # 1. 保存上传的视频文件到服务器
    file_path = VIDEO_STORAGE_PATH / f"{current_user.id}_{datetime.datetime.now().timestamp()}_{video_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)
    
    # 2.在数据库中创建 ClassSession 记录
    session_create = session_schema.SessionCreate(session_name=session_name, session_type=SessionType.OFFLINE.value)
    new_session = crud.create_class_session(db=db, session=session_create, owner_id=current_user.id)

    # 3.在数据库中创建AnalysisTask 记录，并关联到 session
    crud.create_analysis_task(db=db, session_id=new_session.id, video_path=str(file_path))
    # TODO: 在这里触发Celery后台任务，将 new_session.id 传递给它
    # E.g., process_video_task.delay(new_session.id)
    
    # 4. 返回新创建的 session 信息
    return new_session

@router.get("/", response_model=List[session_schema.Session])
def read_sessions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    """
    获取当前的登录用户的所有的会话的列表
    """
    sessions = crud.get_sessions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return sessions