# 课程会话，就是课程的记录

import datetime
import shutil
from pathlib import Path
from typing import List, Any

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
@router.post("/", response_model=session_schema.Session) # response_model 应该是 schemas.Session 而不是 Create
def create_session_with_video_upload(
    *,
    db: Session = Depends(deps.get_db),
    # ↓↓↓ 参数更新点 ↓↓↓
    session_name: str = Form(...),
    layout_id: int = Form(...), # <--- 新增：接收布局ID
    video_file: UploadFile = File(...),
    # ↑↑↑ 参数更新点 ↑↑↑
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建一个新的离线分析会话，关联一个教室布局，并上传视频。
    - 需要用户认证。
    - 接收: 视频文件, 会话名称, 教室布局ID (layout_id).
    """
    
    # 1.【新增】验证 layout_id 是否有效且属于当前用户
    layout = crud.get_layout(db, layout_id=layout_id)
    if not layout:
        raise HTTPException(
            status_code=404, 
            detail=f"Layout with id {layout_id} not found."
        )
    if layout.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to use this layout."
        )
 
    # 2. 保存上传的视频文件到服务器 (您的原始逻辑)
    # 使用更健壮的文件名以避免冲突
    file_path = VIDEO_STORAGE_PATH / f"{current_user.id}_{layout_id}_{datetime.datetime.now().timestamp()}_{video_file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)
    
    # 3. 在数据库中创建 ClassSession 记录 (您的原始逻辑，但已更新)
    # ↓↓↓ 更新点：在创建数据中加入 layout_id ↓↓↓
    session_create = session_schema.SessionCreate(
        name=session_name, 
        # description=... 如果需要也可以从Form中接收
        layout_id=layout_id, # <--- 将验证过的 layout_id 传入
        # session_type=SessionType.OFFLINE.value # 假设您有这个字段
    )
    # 注意：确保您的 crud.create_session_for_user 函数能处理 layout_id
    # 我们之前的修改已经保证了这一点
    new_session = crud.create_session_for_user(db=db, session_in=session_create, user_id=current_user.id)
 
    # 4. 在数据库中创建AnalysisTask 记录 (您的原始逻辑)
    # 假设您的 crud.create_analysis_task 存在
    # crud.create_analysis_task(db=db, session_id=new_session.id, video_path=str(file_path))
    
    # 5. 【可选】触发Celery后台任务
    # process_video_task.delay(new_session.id, str(file_path))
    
    # 6. 返回新创建的 session 信息
    # 为了返回包含完整layout信息的会话，最好重新从数据库查询一次
    db.refresh(new_session)
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

@router.get("/{session_id}", response_model=session_schema.Session)
def read_single_session(
    *,
    session: models.ClassSession = Depends(deps.get_session_by_id_for_owner)

):
    """
    【新】获取单个会话的详细信息。
    只有会话的所有者或管理员才能访问。
    """
    return session

@router.delete("/{session_id}", response_model=session_schema.Session)
def delete_single_session(
    *,
    db: Session =Depends(deps.get_db),
    session_to_delete: models.ClassSession = Depends(deps.get_session_by_id_for_owner)

):
    """
    删除一个会话。
    只有会话的所有者才能删除。
    """
    deleted_session = crud.delete_session(db=db, db_obj=session_to_delete)
    return deleted_session