from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional, List

# 导入未来的 Report Schema
from .report import Report
from .layout import ClassroomLayout
from app.db.models import SessionType

# 基类，包含了创建和读取时都需要的字段
class SessionBase(BaseModel):
    session_name: str
    layout_id: Optional[int] = None
    
# 创建会话时，API端点需要接收的字段
class SessionCreate(SessionBase):
    # session_type 将在端点中根据是上传文件还是实时流来硬编码，
    # 或者也可以让前端传递
    session_type: SessionType # 'offline' or 'realtime'

# 从数据库读取数据并用于API响应的模型
class Session(SessionBase):
    id: int
    owner_id: int
    session_status: str
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None

    # 关系：一个会话有多个分析报告
    reports: List[Report] = []
    # ↓↓↓ 读取会话详情时，可以完整带出其使用的布局信息
    layout: Optional[ClassroomLayout] = None
 

    model_config = ConfigDict(from_attributes=True)
