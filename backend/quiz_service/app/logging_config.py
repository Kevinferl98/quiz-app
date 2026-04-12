import logging
import logging.config
from app.config import config
from app.logging.json_formatter import JsonFormatter

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "()": JsonFormatter,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": config.LOG_LEVEL
        }
    },

    "root": {
        "level": config.LOG_LEVEL,
        "handlers": ["console"]
    },

    "loggers": {
        "pymongo": {
            "level": "WARNING",
            "propagate": False
        },
        "uvicorn": {
            "level": "INFO"
        },
        "uvicorn.error": {
            "level": "INFO"
        },
        "uvicorn.access": {
            "level": "WARNING"
        }
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)