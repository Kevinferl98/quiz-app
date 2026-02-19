from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.logging_config import setup_logging
from app.middleware.logging_middleware import setup_http_logging
from app.services.quiz_grpc_server import serve as serve_grpc

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(serve_grpc())
    print("gRPC server stated on port 50051")

    yield

    grpc_task.cancel()
    print("gRPC server stopped")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_http_logging(app)
app.include_router(router)