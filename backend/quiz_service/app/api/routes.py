import logging
from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.schemas.quiz import (
    AnswerResponse, AnswerRequest, QuizzesResponse,
    QuizCreateRequest, QuizCreateResponse, QuizDeleteResponse, QuizOut, QuizDetailResponse,
    QuestionOut
)
from app.services.quiz_service import QuizService
from app.dependencies import get_quiz_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quizzes", tags=["quizzes"])

DB_ERROR_MSG = "An unexpected error occurred while accessing the database"

@router.get("/public", response_model=QuizzesResponse)
def list_public_quizzes(service: QuizService = Depends(get_quiz_service)):
    try:
        quizzes = service.list_public_quizzes()
        logger.info(f"Returned {len(quizzes)} public quizzes")

        quizzes_out = [QuizOut(title=q["title"], quizId=q["quizId"]) for q in quizzes]
        return QuizzesResponse(quizzes=quizzes_out)
    except Exception as e:
        logger.error(f"DB error listing public quizzes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=DB_ERROR_MSG)

@router.get("/mine", response_model=QuizzesResponse)
def list_my_quizzes(user=Depends(get_current_user), service: QuizService = Depends(get_quiz_service)):
    if not user:
        logger.warning("Unauthorized attempt to list personal quizzes")
        raise HTTPException(status_code=403, detail="Login required")
    
    try:
        quizzes = service.list_personal_quizzes(user["sub"])
        logger.info(f"User {user['sub']} retrieved {len(quizzes)} personal quizzes")
        quizzes_out = [QuizOut(title=q["title"], quizId=q["quizId"]) for q in quizzes]
        return QuizzesResponse(quizzes=quizzes_out)
    except Exception as e:
        logger.error(f"DB error listing personal quizzes for user {user['sub']}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=DB_ERROR_MSG)

@router.get("/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz(quiz_id: str, service: QuizService = Depends(get_quiz_service)):
    try:
        quiz = service.get_quiz_by_id(quiz_id)
        if not quiz:
            logger.warning(f"Quiz {quiz_id} not found")
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        questions_out = [
            QuestionOut(
                id=q["id"],
                question_text=q["question_text"],
                options=q["options"]
            ) for q in quiz.get("questions", [])
        ]
        
        logger.info(f"Quiz {quiz_id} retrieved successfully")
        return QuizDetailResponse(
            quizId=quiz["quizId"],
            title=quiz["title"],
            description=quiz.get("description"),
            questions=questions_out
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DB error fetching quiz {quiz_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=DB_ERROR_MSG)

@router.post("/", response_model=QuizCreateResponse)
def create_quiz(quiz: QuizCreateRequest, user=Depends(get_current_user), service: QuizService = Depends(get_quiz_service)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    
    try:
        quiz_id = service.create_quiz(
            quiz_data=quiz,
            owner_id=user["sub"]
        )
        logger.info(f"User {user['sub']} created quiz {quiz_id}")
        return QuizCreateResponse(success=True, quizId=quiz_id)
    except Exception as e:
        logger.error(f"DB error creating quiz for user {user['sub']}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=DB_ERROR_MSG)

@router.delete("/{quiz_id}", response_model=QuizDeleteResponse)
def delete_quiz(quiz_id: str, user=Depends(get_current_user), service: QuizService = Depends(get_quiz_service)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    try:
        service.delete_quiz(quiz_id=quiz_id, user_id=user["sub"])
        logger.info(f"User {user['sub']} deleted quiz {quiz_id}")
        return QuizDeleteResponse(success=True)
    except ValueError:
        raise HTTPException(status_code=404, detail="Quiz not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="You can only delete your own quizzes")
    except Exception as e:
        logger.error(f"DB error deleting quiz {quiz_id} for user {user['sub']}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=DB_ERROR_MSG)
    
@router.post("/{quiz_id}/answer", response_model=AnswerResponse)
def answer_question(quiz_id: str, payload: AnswerRequest, service: QuizService = Depends(get_quiz_service)):
    try:
        correct = service.check_answer(quiz_id, payload.question_id, payload.answer)
        return AnswerResponse(correct=correct)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))