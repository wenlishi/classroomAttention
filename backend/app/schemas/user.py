import enum
import re
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional, List
from .session import Session

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

    # 2. 定义一个更强大的密码验证器
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        # 'v' 是密码的值
        if len(v) < 8:
            raise ValueError("密码长度至少为8个字符")
            
        # 3. 使用正则表达式检查复杂度
        if not re.search(r'[A-Z]', v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not re.search(r'[a-z]', v):
            raise ValueError("密码必须包含至少一个小写字母")
        if not re.search(r'[0-9]', v):
            raise ValueError("密码必须包含至少一个数字")
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError("密码必须包含至少一个特殊字符 (@$!%*?&)")
            
        return v

# 用于从数据库读取数据时的基类
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

# 用于API响应的模型 (输出)
# 不应包含密码
class User(UserInDBBase):
    # 关系：一个用户可以有多个会话
    sessions: List[Session] = []
 
# 用于API响应用户列表时，可以不包含详细的sessions
class UserSimple(UserInDBBase):
    pass
