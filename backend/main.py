"""时叠 Chronoscope 后端入口。

W3-D1：先提供健康检查接口，确认前后端能通。
后续接口按任务表推进：W4-D1 照片上传与数据库，W5-D2 审核，W6-D1 配准结果查询。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="时叠 Chronoscope API",
    description="校园历史影像三维定位与定年平台",
    version="0.1.0",
    docs_url="/docs",
)

# 前端开发时跑在 5173 端口，需要允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    """健康检查：前端页面角落用它显示后端是否在线。"""
    return {"status": "ok", "version": app.version}
