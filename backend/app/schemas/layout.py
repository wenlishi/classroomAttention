from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING
import datetime
if TYPE_CHECKING:
    from .session import Session # <--- 只有类型检查时才导入，避免循环
 

# --- Desk Schemas ---
class DeskBase(BaseModel):
    pos_x: float
    pos_y: float
    row_num: Optional[int] = None
    col_num: Optional[int] = None
    label: Optional[str] = None
 
class DeskCreate(DeskBase):
    pass # 创建时只需要这些基础信息
 
class Desk(DeskBase):
    id: int
    layout_id: int
 
    model_config = {
        "from_attributes": True
    }
 
# --- ClassroomLayout Schemas ---
class ClassroomLayoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    total_rows: Optional[int] = None
    total_cols: Optional[int] = None
    # ↓↓↓ 新增字段，但设为可选，因为读取时可能没有 ↓↓↓
    background_image_url: Optional[str] = None
 
class ClassroomLayoutCreate(ClassroomLayoutBase):
    # 创建布局时，需要同时提供所有桌子的信息
    desks: List[DeskCreate] = []
     # 创建时不再需要background_image_url，因为它从文件上传中来
 
class ClassroomLayout(ClassroomLayoutBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # 读取一个完整的布局时，把它的所有桌子信息也一并返回
    desks: List[Desk] = [] 
     # sessions: List["Session"] = [] # 如果你想查看一个布局被哪些会话使用了，可以加上这个
 
    model_config = {
        "from_attributes": True
    }