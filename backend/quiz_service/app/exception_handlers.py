from fastapi import Request, status
from fastapi.responses import JSONResponse

def quiz_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Quiz not found"}
    )

def question_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Question not found"}
    )

def permission_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Not allowed"}
    )

def db_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Service temporarily unavailable"}
    )