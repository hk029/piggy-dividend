"""
小猪股息罐 - Python 后端
基于 FastAPI + akshare
"""

import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.quote import router as quote_router
from api.dividend import router as dividend_router
from api.basic import router as basic_router
from api.search import router as search_router, preload_stock_list


# 内存缓存
cache = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("🐷 小猪股息罐服务启动中...")
    
    # 预加载股票列表
    print("📚 正在预加载股票列表...")
    start_time = time.time()
    preload_stock_list()
    print(f"✅ 股票列表预加载完成 (耗时: {time.time() - start_time:.2f}秒)")
    
    yield
    print("👋 服务关闭")


app = FastAPI(
    title="小猪股息罐 API",
    description="股息投资追踪服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(quote_router, prefix="/api", tags=["行情"])
app.include_router(dividend_router, prefix="/api", tags=["分红"])
app.include_router(basic_router, prefix="/api", tags=["基础信息"])
app.include_router(search_router, prefix="/api", tags=["搜索"])


@app.get("/")
async def root():
    return {
        "name": "小猪股息罐 API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
