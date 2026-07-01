"""
分红数据接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

router = APIRouter()

# 缓存配置
CACHE_TTL = 7 * 86400  # 7天缓存（分红数据很少变化，有新分红时覆盖）
dividend_cache = {}


class DividendRecord(BaseModel):
    symbol: str
    year: Optional[str] = None
    dividend_per_share: float
    announce_date: Optional[str] = None
    ex_dividend_date: Optional[str] = None
    payment_date: Optional[str] = None
    record_date: Optional[str] = None


class DividendSummary(BaseModel):
    symbol: str
    annual_dividend: float  # 最近一年每股分红
    dividend_yield: float  # 股息率（需要配合当前价格计算）
    last_dividend_date: Optional[str] = None
    records: List[DividendRecord]


def get_cache_key(symbol: str) -> str:
    return f"dividend:{symbol}"


def is_cache_valid(key: str) -> bool:
    if key in dividend_cache:
        cached_time, _ = dividend_cache[key]
        if time.time() - cached_time < CACHE_TTL:
            return True
    return False


@router.get("/dividend/{symbol}")
async def get_dividend(symbol: str):
    """获取股票分红记录"""
    cache_key = get_cache_key(symbol)

    # 检查缓存
    if is_cache_valid(cache_key):
        return dividend_cache[cache_key][1]

    try:
        import akshare as ak

        # 尝试获取分红数据
        # akshare 的分红接口
        try:
            df = ak.stock_history_dividend_detail(symbol=symbol, indicator="分红")
        except Exception:
            # 如果 akshare 接口失败，返回空数据
            df = None

        records = []
        annual_dividend = 0.0
        ttm_dividend = 0.0  # TTM分红（过去12个月）

        if df is not None and not df.empty:
            from datetime import datetime, timedelta
            
            # 用于按年份汇总分红
            yearly_dividend = {}
            
            # 获取当前日期
            now = datetime.now()
            one_year_ago = now - timedelta(days=365)
            
            for _, row in df.head(10).iterrows():  # 最近10次分红记录
                # 列名: 公告日期, 送股, 转增, 派息, 进度, 除权除息日, 股权登记日, 红股上市日
                announce_date = str(row.get("公告日期", "")) or None
                year = announce_date[:4] if announce_date else ""
                
                # 除权除息日才是实际分红日期
                ex_date_str = str(row.get("除权除息日", "")) or None
                
                # 注意："派息"是每10股的金额，需要除以10得到每股分红
                dividend_per_10_shares = float(row.get("派息", 0) or 0)
                dividend_per_share = dividend_per_10_shares / 10
                
                record = DividendRecord(
                    symbol=symbol,
                    year=year,
                    dividend_per_share=dividend_per_share,
                    announce_date=announce_date,
                    ex_dividend_date=ex_date_str,
                    payment_date=None,
                    record_date=str(row.get("股权登记日", "")) or None,
                )
                records.append(record)
                
                # 按年份汇总分红
                if year:
                    if year not in yearly_dividend:
                        yearly_dividend[year] = 0
                    yearly_dividend[year] += dividend_per_share
                
                # 计算TTM分红（过去12个月内的分红）
                if ex_date_str:
                    try:
                        ex_date = datetime.strptime(ex_date_str, "%Y-%m-%d")
                        if ex_date >= one_year_ago:
                            ttm_dividend += dividend_per_share
                    except:
                        pass

            # 年度分红计算策略：
            # 1. 优先使用TTM（过去12个月）数据
            # 2. 如果TTM数据不足，使用最近完整年度的数据
            current_year = str(now.year)
            last_year = str(now.year - 1)
            
            if ttm_dividend > 0:
                annual_dividend = ttm_dividend
                dividend_type = "TTM"
            elif current_year in yearly_dividend:
                annual_dividend = yearly_dividend[current_year]
                dividend_type = current_year
            elif last_year in yearly_dividend:
                annual_dividend = yearly_dividend[last_year]
                dividend_type = last_year
            else:
                latest_year = max(yearly_dividend.keys()) if yearly_dividend else "0"
                annual_dividend = yearly_dividend.get(latest_year, 0)
                dividend_type = latest_year
            
            print(f"[{symbol}] 年度分红: {yearly_dividend}, TTM: {ttm_dividend}, 选用: {dividend_type}={annual_dividend}")

        result = {
            "symbol": symbol,
            "annual_dividend": annual_dividend,
            "dividend_yield": 0,  # 需要配合实时价格计算
            "last_dividend_date": records[0].payment_date if records else None,
            "records": [r.dict() for r in records],
        }

        # 更新缓存
        dividend_cache[cache_key] = (time.time(), result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分红数据失败: {str(e)}")


@router.get("/dividend/{symbol}/yield")
async def get_dividend_yield(symbol: str, price: float):
    """计算实时股息率"""
    try:
        dividend_data = await get_dividend(symbol)

        if dividend_data["annual_dividend"] > 0 and price > 0:
            yield_pct = (dividend_data["annual_dividend"] / price) * 100
        else:
            yield_pct = 0

        return {
            "symbol": symbol,
            "price": price,
            "annual_dividend": dividend_data["annual_dividend"],
            "dividend_yield": round(yield_pct, 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算股息率失败: {str(e)}")
