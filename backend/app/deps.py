from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
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
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token" 
)

def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
): 
    """
    解码token以获取用户名，然后从数据库中检索用户。
    这是获取用户对象的基础依赖，但不检查用户是否激活。
    """
    # 解码token

    username = security.decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}

        )
    # 从数据库获取用户
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="不存在的用户"
        )
    return user
 
def get_current_active_user(current_user: models.User=Depends(get_current_user),):
    """
    一个依赖于 get_current_user 的依赖项。
    它只做一件事：检查从token中获取的用户是否处于激活状态。
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

    