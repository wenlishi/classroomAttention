from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import auth, sessions, users, layouts
from app.db import database, models


app = FastAPI(title="classroom Atttention")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置CORS（跨域资源共享），允许前端访问
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- 使用上面定义的 origins 列表
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 2. 在这里添加 CORS 中间件配置
# 如果 settings.BACKEND_CORS_ORIGINS 存在并且已配置, 则使用它




api_v1_prefix = "/api/v1"
# 包含WebSocket路由
app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth", tags=["auth"])
app.include_router(sessions.router, prefix=f"{api_v1_prefix}/sessions", tags=["sessions"])
app.include_router(users.router, prefix=f"{api_v1_prefix}/users", tags=["users"])
app.include_router(layouts.router, prefix=f"{api_v1_prefix}/layouts", tags=["layouts"])
