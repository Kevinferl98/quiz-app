from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.api.routes import router
from app.exception import (
    QuizNotFoundError,
    QuestionNotFoundError,
    QuizPermissionError,
    DatabaseError
)
from app.exception_handlers import (
    quiz_not_found_handler,
    question_not_found_handler,
    permission_error_handler,
    db_error_handler
)
from app.logging_config import setup_logging
from app.middleware.logging_middleware import setup_http_logging
from app.services.quiz_grpc_server import serve as serve_grpc
from app.db.mongo_client import mongo_db

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(serve_grpc())
    print("gRPC server stated on port 50051")
    mongo_db.connect()

    yield

    grpc_task.cancel()
    print("gRPC server stopped")
    mongo_db.close()

app = FastAPI(lifespan=lifespan)

setup_http_logging(app)
app.include_router(router)

app.add_exception_handler(QuizNotFoundError, quiz_not_found_handler)
app.add_exception_handler(QuestionNotFoundError, question_not_found_handler)
app.add_exception_handler(QuizPermissionError, permission_error_handler)
app.add_exception_handler(DatabaseError, db_error_handler)