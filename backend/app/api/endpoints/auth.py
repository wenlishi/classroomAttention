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
from app.deps import get_db
from app import crud






# 创建一个API路由器的实例
router = APIRouter()

# --- 用户注册端点 --- 
@router.post("/register", response_model=user_schema.UserSimple,status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schema.UserCreate
):
    """
    创建新用户.
    - 接收用户名和密码邮箱和角色.
    - 检查用户名是否已存在.
    - 对密码进行哈希处理.
    - 将新用户存入数据库.
    - 返回创建后的用户信息 (不含密码).
    """
    #1. 检查数据库中是否已存在该用户
    db_user = crud.get_user_by_username(db,username=user_in.username)
    
    if db_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",

        )
    
    return crud.create_user(db,user=user_in)



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
    # 1. 调用 CRUD 函数去验证用户
    #    注意：它的返回值是 user 对象或者 None，不抛出 HTTP 异常
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    
     # 2.验证用户是否存在以及密码是否正确
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或者密码不正确",
            headers={"WWW-Authenticate":"Bearer"}# 这是OAuth2.0规范的一部分
         )
    # 3.创建JWT
    # JWT的"subject" (sub)通常用来存放用户的唯一标识符
    access_token = security.create_access_token(data={"sub":user.username})
    # 正确的返回方式：返回一个符合 `Token` schema 的字典
    return {"access_token": access_token, "token_type": "bearer"}

   
