import os
from typing import Generator
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.database import SessionLocal
from app.db import models
from app.core import security
from app.db.models import UserRole
from app import crud



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



# 这个对象会从请求的 Authorization header 中寻找 Bearer Token
# tokenUrl 指向你的登录接口，FastAPI会在交互式文档中用它来获取token
# 这个函数将作为我们新的、主要的依赖项

async def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> models.User:
    """
    从请求的 HttpOnly Cookie 中提取、解码并验证 token，
    然后返回对应的用户模型。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token")

    if token is None:
        raise credentials_exception

    if token.startswith("Bearer "):
        token = token.split("Bearer ", 1)[1]

    # [核心修改] 2. 直接调用您的解码函数
    username = security.decode_access_token(token)
    if not username:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# 您的 get_current_active_user 函数现在应该依赖于上面的 get_current_user
async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    检查从 token 中获取的用户是否处于激活状态。
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="未激活的用户")
    return current_user

def get_current_admin_user(
        current_user: models.User = Depends(get_current_active_user),
):
    """
    一个依赖项，用于：
    1. 检查用户是否已登录且是激活的 (通过复用 get_current_active_user)。
    2. 检查用户的角色是否为 'admin'。
    如果不是管理员，则抛出403 Forbidden错误。
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="当前用户没有足够的权限"

        )
    return current_user



def get_session_by_id_for_owner(
        session_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user),    
)-> models.ClassSession:
    session = crud.get_session(db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return session

    