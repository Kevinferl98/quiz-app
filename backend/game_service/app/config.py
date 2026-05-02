import os

class Config:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t") or ENV == "development"
    TESTING = ENV == "testing"
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")
    _OTEL_ENABLED_ENV = os.getenv("OTEL_ENABLED", "true").lower() in ("true", "1", "t")
    OTEL_ENABLED = _OTEL_ENABLED_ENV and not TESTING
    OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "game_service")
    OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")
    OTEL_TRACES_SAMPLER = os.getenv("OTEL_TRACES_SAMPLER", "parentbased_traceidratio")
    OTEL_TRACES_SAMPLER_ARG = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0"))
    HTTP_LOG_BODIES = os.getenv("HTTP_LOG_BODIES", "false").lower() in ("true", "1", "t")
    HTTP_LOG_MAX_BODY_BYTES = int(os.getenv("HTTP_LOG_MAX_BODY_BYTES", "4096"))


config = Config()
