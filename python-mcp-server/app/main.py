from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .models import TickerResponse, OHLCVResponse, ErrorResponse
from .exchanges import fetch_ticker, fetch_ohlcv, close_exchanges
from .cache import get_cached, set_cached
from .settings import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ticker/{exchange}/{symbol}")
async def get_ticker(exchange: str, symbol: str):
    try:
        raw = await fetch_ticker(exchange, symbol)
        return raw
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historical/{exchange}/{symbol}")
async def get_hist(exchange: str, symbol: str, timeframe='1m', since=None, limit=100):
    try:
        data = await fetch_ohlcv(exchange, symbol, timeframe, since, limit)
        return {"exchange": exchange, "symbol": symbol, "ohlcv": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown():
    await close_exchanges()
