from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Python MCP Crypto Server"
    POLL_INTERVAL_SECONDS: int = 5
    CACHE_TTL_SECONDS: int = 10
    CCXT_TIMEOUT: int = 10
    COINMARKETCAP_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
