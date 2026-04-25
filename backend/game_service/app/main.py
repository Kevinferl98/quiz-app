from fastapi import FastAPI
from app.api.routes import router
from app.api.routes_ws import router_ws
from app.logging_config import setup_logging
from app.middleware.logging_middleware import setup_http_logging
from app.dependencies import get_room_manager

setup_logging()
app = FastAPI()
setup_http_logging(app)

app.include_router(router)
app.include_router(router_ws)

@app.on_event("startup")
async def startup():
    manager = get_room_manager()
    await manager.start()

@app.on_event("shutdown")
async def shutdown():
    manager = get_room_manager()
    await manager.stop()