from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, sessions, users
from app.db import database, models


app = FastAPI(title="classroom Atttention")

# 配置CORS（跨域资源共享），允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1_prefix = "/api/v1"
# 包含WebSocket路由
app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth", tags=["auth"])
app.include_router(sessions.router, prefix=f"{api_v1_prefix}/sessions", tags=["sessions"])
app.include_router(users.router, prefix=f"{api_v1_prefix}/users", tags=["users"]) # <-- 2. 包含这行
