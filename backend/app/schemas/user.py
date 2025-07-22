import enum
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# 1. 创建一个角色枚举类
class UserRole(str, enum.Enum):
    TEACHER = "teacher"
    # 如果未来有其他角色，比如 admin，可以加在这里
    ADMIN = "admin"

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
    email: EmailStr # 使用EmailStr可以自动验证邮件格式
    role: UserRole = UserRole.TEACHER  # 提供了默认值

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
    