from pydantic import BaseModel,ConfigDict
from typing import Optional

#Token相关的Schema
class Token(BaseModel):
    access_token: str 
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- User相关的Schema ---
# 这是所有User模型的基类，包含通用字段
class UserBase(BaseModel):
    username: str

# 用于创建用户时接收的数据 (输入)
# 需要密码
class UserCreate(UserBase):
    password: str

# 用于从数据库读取数据时的基类
class UserInDBBase(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 用于API响应的模型 (输出)
# 注意：这个模型不包含任何敏感信息，如密码哈希
class UserInDB(UserInDBBase):
    pass
    