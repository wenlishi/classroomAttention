from datetime import datetime,timedelta,timezone
from typing import Optional 
from jose import JWTError,jwt
from passlib.context import CryptContext

from app.core.config import settings

# 创建一个密码上下文，用于哈希和验证密码
# 我们使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password: str, hashed_password: str)-> bool:
    """验证明文密码和哈希密码是否匹配"""
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password: str)->str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ 创建JWT访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 如果没有提供过期时间的话，则使用配置中的默认的时间
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encode_jwt



def decode_access_token(token: str):
    """
    解码 access token.
    :param token: a JWT token.
    :return: a username if token is valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username 
    except JWTError:
        return  None
    