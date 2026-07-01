"""
股票搜索接口
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()

# 缓存
search_cache = {}
CACHE_TTL = 86400  # 1天

# 股票列表缓存（全局）
_stock_list_cache = None
_stock_list_cache_time = 0
STOCK_LIST_CACHE_TTL = 86400  # 24小时


class StockSearchResult(BaseModel):
    symbol: str
    name: str
    market: Optional[str] = None
    industry: Optional[str] = None


def preload_stock_list():
    """预加载股票列表（启动时调用）"""
    global _stock_list_cache, _stock_list_cache_time
    
    try:
        import akshare as ak
        df = ak.stock_info_a_code_name()
        if df is not None and not df.empty:
            _stock_list_cache = df
            _stock_list_cache_time = time.time()
            return True
    except Exception as e:
        print(f"预加载股票列表失败: {e}")
    return False


def get_stock_list():
    """获取股票列表（带缓存）"""
    global _stock_list_cache, _stock_list_cache_time
    
    # 如果已缓存，直接返回
    if _stock_list_cache is not None:
        return _stock_list_cache
    
    # 否则尝试加载
    return _stock_list_cache if preload_stock_list() else None


@router.get("/search", response_model=List[StockSearchResult])
async def search_stocks(
    keyword: str = Query(..., min_length=1, description="搜索关键词（股票代码或名称）"),
    limit: int = Query(10, ge=1, le=50, description="返回数量")
):
    """
    搜索股票（支持代码和名称模糊匹配）
    """
    cache_key = f"search:{keyword}:{limit}"
    
    # 检查缓存
    if cache_key in search_cache:
        cached_time, cached_data = search_cache[cache_key]
        if time.time() - cached_time < CACHE_TTL:
            print(f"[{time.strftime('%H:%M:%S')}] 缓存命中: {keyword}")
            return cached_data

    try:
        df = get_stock_list()
        
        if df is None or df.empty:
            print(f"[{time.strftime('%H:%M:%S')}] 股票列表为空")
            return []
        
        # 模糊匹配代码或名称
        print(f"[{time.strftime('%H:%M:%S')}] 搜索关键词: {keyword}")
        mask = (
            df['code'].str.contains(keyword, case=False, na=False) |
            df['name'].str.contains(keyword, case=False, na=False)
        )
        
        filtered = df[mask].head(limit)
        print(f"[{time.strftime('%H:%M:%S')}] 找到 {len(filtered)} 条结果")
        
        results = []
        for _, row in filtered.iterrows():
            code = str(row.get('code', ''))
            name = str(row.get('name', ''))
            
            # 判断市场
            market = detect_market(code)
            
            results.append(StockSearchResult(
                symbol=code,
                name=name,
                market=market,
                industry=None,
            ))
        
        # 更新缓存
        search_cache[cache_key] = (time.time(), results)
        
        return results
        
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] 搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return []


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
    return "未知"
