import asyncio
from cachetools import TTLCache

_cache = TTLCache(maxsize=1024, ttl=10)
_cache_lock = asyncio.Lock()

async def get_cached(key: str):
    async with _cache_lock:
        return _cache.get(key)

async def set_cached(key: str, value, ttl: int = None):
    async with _cache_lock:
        if ttl is not None:
            _cache.ttl = ttl
        _cache[key] = value
