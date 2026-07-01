"""
实时行情接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()

# 缓存配置
CACHE_TTL = 60  # 60秒缓存
quote_cache = {}
quote_update_time = {}  # 记录每只股票的更新时间


class QuoteResponse(BaseModel):
    symbol: str
    name: Optional[str] = None
    price: float
    change: float
    change_pct: float
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    amount: Optional[float] = None
    timestamp: float


class BatchQuoteRequest(BaseModel):
    symbols: List[str]


def get_cache_key(symbol: str) -> str:
    return f"quote:{symbol}"


def is_cache_valid(key: str) -> bool:
    if key in quote_cache:
        cached_time, _ = quote_cache[key]
        if time.time() - cached_time < CACHE_TTL:
            return True
    return False


@router.get("/quote/{symbol}")
async def get_quote(symbol: str):
    """获取单只股票实时行情"""
    cache_key = get_cache_key(symbol)

    # 检查缓存
    if is_cache_valid(cache_key):
        return quote_cache[cache_key][1]

    try:
        # 使用 akshare 获取实时行情
        import akshare as ak
        
        # 根据代码判断市场
        if symbol.startswith("6"):
            # 沪市
            df = ak.stock_zh_a_spot_em()
        else:
            # 深市
            df = ak.stock_zh_a_spot_em()
        
        if df is not None and not df.empty:
            # 查找对应股票
            stock_row = df[df["代码"] == symbol]
            if not stock_row.empty:
                row = stock_row.iloc[0]
                result = {
                    "symbol": symbol,
                    "name": row.get("名称", ""),
                    "price": float(row.get("最新价", 0) or 0),
                    "change": float(row.get("涨跌额", 0) or 0),
                    "change_pct": float(row.get("涨跌幅", 0) or 0),
                    "open": float(row.get("今开", 0) or 0),
                    "high": float(row.get("最高", 0) or 0),
                    "low": float(row.get("最低", 0) or 0),
                    "volume": int(row.get("成交量", 0) or 0),
                    "amount": float(row.get("成交额", 0) or 0),
                    "timestamp": time.time(),
                }
                quote_cache[cache_key] = (time.time(), result)
                quote_update_time[symbol] = time.time()  # 记录更新时间
                return result
        
        raise HTTPException(status_code=404, detail=f"未找到股票 {symbol}")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行情失败: {str(e)}")


@router.post("/quotes")
async def get_batch_quotes(request: BatchQuoteRequest):
    """批量获取股票行情"""
    results = []

    for symbol in request.symbols:
        try:
            quote = await get_quote(symbol)
            # 添加更新时间
            quote["update_time"] = quote_update_time.get(symbol)
            results.append(quote)
        except HTTPException as e:
            results.append({"symbol": symbol, "error": str(e.detail)})

    return {"quotes": results}


@router.get("/quotes/cache")
async def get_quotes_cache():
    """获取所有缓存的行情数据"""
    cached_quotes = []
    for key, (timestamp, data) in quote_cache.items():
        symbol = data.get("symbol", "")
        cached_quotes.append({
            "symbol": symbol,
            "name": data.get("name", ""),
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "update_time": quote_update_time.get(symbol),
            "cache_time": timestamp,
        })
    return {"quotes": cached_quotes, "count": len(cached_quotes)}
