from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth
from app.db import database, models

# 创建数据库表
print("正在尝试创建数据库表...")
models.Base.metadata.create_all(bind=database.engine)
print("数据库创建成功！")

app = FastAPI(title="classroom Atttention")

# 配置CORS（跨域资源共享），允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含WebSocket路由
app.include_router(auth.router)
