import time
import logging
from fastapi import Request, FastAPI

logger = logging.getLogger("app.middleware.logging")

def setup_http_logging(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        client_host = request.client.host if request.client else "unknown"
        path = request.url.path
        method = request.method

        response = await call_next(request)

        process_time_ms = (time.time() - start_time) * 1000
        
        log_msg = (
            f"ID: {method} {path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time_ms:.2f}ms | "
            f"IP: {client_host}"
        )

        if response.status_code >= 500:
            logger.error(log_msg)
        else:
            logger.info(log_msg)

        return response