"""
股票基础信息接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter()

# 缓存配置
CACHE_TTL = 604800  # 7天缓存（基础信息很少变动）
basic_cache = {}


class BasicInfoResponse(BaseModel):
    symbol: str
    name: str
    market: Optional[str] = None  # 市场：沪市/深市/港股
    industry: Optional[str] = None
    list_date: Optional[str] = None
    total_shares: Optional[int] = None
    float_shares: Optional[int] = None


def get_cache_key(symbol: str) -> str:
    return f"basic:{symbol}"


def is_cache_valid(key: str) -> bool:
    if key in basic_cache:
        cached_time, _ = basic_cache[key]
        if time.time() - cached_time < CACHE_TTL:
            return True
    return False


def detect_market(symbol: str) -> str:
    """根据股票代码判断市场"""
    if symbol.startswith("6"):
        return "沪市"
    elif symbol.startswith("0") or symbol.startswith("3"):
        return "深市"
    elif symbol.startswith("8") or symbol.startswith("4"):
        return "北交所"
    elif len(symbol) == 5:
        return "港股"
    else:
        return "未知"


@router.get("/basic/{symbol}")
async def get_basic_info(symbol: str):
    """获取股票基础信息"""
    cache_key = get_cache_key(symbol)

    # 检查缓存
    if is_cache_valid(cache_key):
        return basic_cache[cache_key][1]

    try:
        import akshare as ak
        
        # 获取股票基础信息
        try:
            df = ak.stock_individual_info_em(symbol=symbol)
        except Exception:
            df = None

        if df.empty:
            # 如果 akshare 没有数据，返回基础信息
            result = {
                "symbol": symbol,
                "name": f"股票{symbol}",
                "market": detect_market(symbol),
                "industry": None,
                "list_date": None,
                "total_shares": None,
                "float_shares": None,
            }
        else:
            row = df.iloc[0]
            result = {
                "symbol": symbol,
                "name": row.get("name", f"股票{symbol}"),
                "market": detect_market(symbol),
                "industry": row.get("industry", None),
                "list_date": row.get("list_date", None),
                "total_shares": int(row.get("total_shares", 0)) if row.get("total_shares") else None,
                "float_shares": int(row.get("float_shares", 0)) if row.get("float_shares") else None,
            }

        # 更新缓存
        basic_cache[cache_key] = (time.time(), result)

        return result

    except Exception as e:
        # 出错时返回基本信息
        result = {
            "symbol": symbol,
            "name": f"股票{symbol}",
            "market": detect_market(symbol),
            "industry": None,
            "list_date": None,
            "total_shares": None,
            "float_shares": None,
        }
        return result
