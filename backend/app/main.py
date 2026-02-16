from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.routes_ws import router_ws
from app.logging_config import setup_logging
from app.middleware.logging_middleware import setup_http_logging

setup_logging()
app = FastAPI()
setup_http_logging(app)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(router_ws)