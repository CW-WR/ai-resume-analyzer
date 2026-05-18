from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_API_BASE_URL: str = os.getenv("AI_API_BASE_URL", "https://api.chatanywhere.tech/v1")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    CACHE_EXPIRE: int = int(os.getenv("CACHE_EXPIRE", "86400"))
    
    class Config:
        env_file = ".env"

settings = Settings()