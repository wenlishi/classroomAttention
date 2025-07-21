import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..'))
print(project_root)
sys.path.insert(0, project_root)
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import models, database
from app.schemas import user as user_schema
from app.core import security 
from app.api.deps import get_db



# 创建一个API路由器的实例
router = APIRouter()

# --- 用户注册端点 --- 
@router.post("/register", response_model=user_schema.UserInDB,status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schema.UserCreate
):
    """
    创建新用户.
    - 接收用户名和密码.
    - 检查用户名是否已存在.
    - 对密码进行哈希处理.
    - 将新用户存入数据库.
    - 返回创建后的用户信息 (不含密码).
    """
    #1. 检查数据库中是否已存在该用户
    db_user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",

        )
    # 2.对密码进行哈希处理
    hashed_password = security.get_password_hash(user_in.password)

    # 3.创建数据库模型实例

    db_user = models.User(
        username=user_in.username,
        hash_password=hashed_password
    )

    # 4. 存入数据库
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # 刷新实例以从数据库获取ID等信息 

    return db_user

# ---用户登录端点---
@router.post("/token",response_model=user_schema.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
     
     
    """
    用户登录以获取JWT.
    - 使用 OAuth2PasswordRequestForm 依赖项, 它会从请求体中解析 'username' 和 'password'.
    - 前端需要以 'application/x-www-form-urlencoded' 格式发送数据.
    - 验证用户凭据.
    - 成功后创建并返回一个access token.
    """
     # 1.在数据库中通过用户名查找用户
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
     # 2.验证用户是否存在以及密码是否正确
    if not user or not security.verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或者密码不正确",
            headers={"WWW-Authenticate":"Bearer"}# 这是OAuth2.0规范的一部分
         )
    # 3.创建JWT
    # JWT的"subject" (sub)通常用来存放用户的唯一标识符
    access_token = security.create_access_token(data={"sub":user.username})
    return access_token



print(router)
   
