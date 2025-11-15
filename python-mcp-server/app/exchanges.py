import ccxt.async_support as ccxt
import asyncio
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential
from typing import Any, Dict, Optional, List
from .settings import settings

_EXCHANGE_INSTANCES = {}
_LOCK = asyncio.Lock()

async def get_exchange(name: str):
    name = name.lower()
    async with _LOCK:
        if name in _EXCHANGE_INSTANCES:
            return _EXCHANGE_INSTANCES[name]
        cls = getattr(ccxt, name, None)
        if cls is None:
            raise ValueError(f"Exchange '{name}' not supported")
        ex = cls({'enableRateLimit': True, 'timeout': settings.CCXT_TIMEOUT * 1000})
        _EXCHANGE_INSTANCES[name] = ex
        return ex

async def fetch_ticker(exchange_name: str, symbol: str):
    ex = await get_exchange(exchange_name)
    async for attempt in AsyncRetrying(
        reraise=True, stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_exception_type(Exception),
    ):
        with attempt:
            return await ex.fetch_ticker(symbol)

async def fetch_ohlcv(exchange_name: str, symbol: str, timeframe='1m', since=None, limit=100):
    ex = await get_exchange(exchange_name)
    async for attempt in AsyncRetrying(
        reraise=True, stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_exception_type(Exception),
    ):
        with attempt:
            return await ex.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)

async def close_exchanges():
    async with _LOCK:
        coros = []
        for ex in _EXCHANGE_INSTANCES.values():
            try:
                coros.append(ex.close())
            except:
                pass
        await asyncio.gather(*coros, return_exceptions=True)
        _EXCHANGE_INSTANCES.clear()
