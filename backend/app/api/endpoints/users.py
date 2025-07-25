from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app import crud, deps
from app.schemas import user as user_schema
from app.db import models



router = APIRouter()

# 获取所有用户列表，只有管理员能调用
@router.get("/", response_model=List[user_schema.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # 核心：使用依赖注入将这个端点保护起来，只有管理员能访问
    current_admin: models.User = Depends(deps.get_current_admin_user),
):
    """
    获取一个用户列表。
    (仅限管理员访问)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    

# 核心功能：更新用户的 is_active 状态
@router.put("/{user_id}/status", response_model=user_schema.User)
def update_user_is_active(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    is_active: bool = Body(..., embed=True), # 从请求体中获取 is_active
    # 核心：确保只有管理员才能执行此操作
    current_admin: models.User = Depends(deps.get_current_admin_user),
):
    """
    激活或禁用一个用户。
    (仅限管理员访问)
    """
    # 从数据库中获取需要被修改的用户
    user_to_update = crud.get_user(db, user_id=user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="未找到该用户")
    
    # 一个重要的安全检查：管理员不能禁用自己
    if user_to_update.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Admins cannot deactivate themselves")
 
    # 使用 crud 层更新用户
    updated_user = crud.update_user_is_active(db=db, user=user_to_update, is_active=is_active)
    
    return updated_user 
