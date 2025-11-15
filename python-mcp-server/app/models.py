from pydantic import BaseModel
from typing import Optional, List, Any

class TickerResponse(BaseModel):
    exchange: str
    symbol: str
    timestamp: int
    datetime: str
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    info: Any

class OHLCVResponse(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    since: Optional[int]
    limit: Optional[int]
    ohlcv: List[List[float]]

class ErrorResponse(BaseModel):
    error: str
