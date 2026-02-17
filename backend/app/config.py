import os

class Config:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t") or ENV == "development"
    TESTING = ENV == "testing"
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")


config = Config()