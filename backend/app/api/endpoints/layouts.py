import shutil
import uuid
import json
import time
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form # 导入File, UploadFile, Form

from pydantic import ValidationError
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

    print(layout_data)
    try:
        layout_in = layout_schema.ClassroomLayoutCreate.model_validate_json(layout_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="The provided layout_data is not a valid JSON.")
    
    except ValidationError as e:
        # 这是最重要的修改！
        # 它会将详细的字段错误信息返回给前端
        raise HTTPException(status_code=422, detail=e.errors()) # 422 状态码是“无法处理的实体”
 
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


@router.get("/me", response_model=List[layout_schema.ClassroomLayout]) 
def read_my_layouts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
)-> Any:
    """
    获取当前用户创建的所有教室布局列表。
    """ 
    # 这部分代码完全不需要动
    layouts = crud.get_layouts_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return layouts

@router.get("/{layout_id}", response_model=layout_schema.ClassroomLayout)
def read_single_layout(
    *,
    db: Session = Depends(deps.get_db),
    layout_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取单个布局的完整信息，包含其中所有的桌子。
    """
    layout = crud.get_layout(db, layout_id=layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    if layout.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return layout

@router.delete("/{layout_id}", response_model=layout_schema.ClassroomLayout)
def delete_single_layout(
    *,
    db: Session = Depends(deps.get_db),
    layout_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    删除一个教室布局（其下的所有桌子也会被一并删除）。
    """
    layout_to_delete = crud.get_layout(db, layout_id=layout_id)
    if not layout_to_delete:
        raise HTTPException(status_code=404, detail="Layout not found")
    if layout_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    deleted_layout = crud.delete_layout(db=db, db_obj=layout_to_delete)
    return deleted_layout