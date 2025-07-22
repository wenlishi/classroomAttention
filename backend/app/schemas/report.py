from pydantic import BaseModel, ConfigDict
import datetime

# 基类
class ReportBase(BaseModel):
    tracked_person_id: int
    attention_score: float
    total_duration: float
    head_up_duration: float

# 创建时使用
class ReportCreate(ReportBase):
    pass

# 用于API响应
class Report(ReportBase):
    id: int
    session_id: int
    report_generated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
