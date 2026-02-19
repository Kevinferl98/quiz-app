from fastapi import FastAPI
from app.api.routes import router
from app.api.routes_ws import router_ws
from app.logging_config import setup_logging
from app.middleware.logging_middleware import setup_http_logging

setup_logging()
app = FastAPI()
setup_http_logging(app)

app.include_router(router)
app.include_router(router_ws)