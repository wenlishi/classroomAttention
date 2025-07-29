import shutil
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form # 导入File, UploadFile, Form

from sqlalchemy.orm import Session
from typing import List, Any, Optional

from app import crud, deps
from app.db import models
from app.schemas import layout as layout_schema


router = APIRouter()

@router.post("/", response_model=layout_schema.ClassroomLayout)
def create_layout(
    *,
    db: Session = Depends(deps.get_db),
    # ↓↓↓ 关键改动：这样接收混合数据 ↓↓↓
    layout_data: str = Form(...), # JSON数据作为字符串接收
    file: Optional[UploadFile] = File(None), # 文件是可选的
    # ↑↑↑ 关键改动 ↑↑↑
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    为当前登录用户创建一个新的教室布局。
    这个端点接收 multipart/form-data，包含:
    - layout_data: 一个包含布局名称、描述和桌子信息的JSON字符串。
    - file: (可选) 一张教室的背景图片。
    """
    # 1. 解析JSON字符串为Pydantic模型
    try:
        layout_in = layout_schema.ClassroomLayoutCreate.model_validate_json(layout_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid layout data format.")
 
    # 2. 如果有文件上传，保存文件并生成URL
    image_url_path = None
    if file:
        # 检查文件类型
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(status_code=400, detail="Invalid image type. Only JPG, PNG, GIF are allowed.")
          
        # 生成唯一文件名，防止覆盖
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        save_path = f"static/uploads/{unique_filename}"
      
        # 保存文件到服务器
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
          
        # 生成可供前端访问的URL路径
        image_url_path = f"/static/uploads/{unique_filename}"
 
    # 3. 调用CRUD函数创建数据库记录
    layout = crud.create_layout_with_desks(
        db=db, 
        layout_in=layout_in, 
        owner_id=current_user.id, 
        image_url=image_url_path # 传入图片URL
    )
    return layout