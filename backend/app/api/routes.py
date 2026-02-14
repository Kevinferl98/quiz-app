from fastapi import APIRouter, Depends, HTTPException
from app.services import quiz_service
from app.auth import get_user_dep
from app.models.quiz import Quiz, AnswerSubmission

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/public")
def list_public_quizzes():
    try:
        quizzes = quiz_service.list_public_quizzes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    return {"quizzes": quizzes}

@router.get("/mine")
def list_my_quizzes(user=Depends(get_user_dep)):
    if not user:
        raise HTTPException(status_code=403, detail="Login required")
    
    try:
        quizzes = quiz_service.list_personal_quizzes(user["sub"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"quizzes": quizzes}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str, user=Depends(get_user_dep)):
    try:
        quiz = quiz_service.get_quiz_by_id(quiz_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz

@router.post("/")
def create_quiz(quiz: Quiz, user=Depends(get_user_dep)):    
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    
    try:
        quiz_id = quiz_service.create_quiz(
            quiz_data=quiz.model_dump(),
            owner_id=user["sub"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"success": True, "quizId": quiz_id}

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str, user=Depends(get_user_dep)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    try:
        quiz_service.delete_quiz(
            quiz_id=quiz_id,
            user_id=user["sub"]
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Quiz not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="You can only delete your own quizzes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"success": True}

@router.post("/{quiz_id}/submit")
def submit_quiz(
    quiz_id: str,
    submission: AnswerSubmission,
    user=Depends(get_user_dep)
):
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")

    try:
        result = quiz_service.submit_quiz(
            quiz_id=quiz_id,
            answers=submission.answers,
            user_id=user["sub"]
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Quiz not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return result