"""
FastAPI主应用
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import API_PREFIX
from api import upload, analyze, results

# 创建FastAPI应用
app = FastAPI(
    title="DeepInsight Platform API",
    description="基于LSTM的电商产品分析可视化Web平台API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(upload.router, prefix=API_PREFIX)
app.include_router(analyze.router, prefix=API_PREFIX)
app.include_router(results.router, prefix=API_PREFIX)
# 注册符合设计文档的reviews路由
app.include_router(results.reviews_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "DeepInsight Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

