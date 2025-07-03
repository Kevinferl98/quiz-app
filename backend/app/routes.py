from fastapi import APIRouter, Depends, HTTPException
import uuid
from app.models import Quiz
from app.db.dynamodb_client import quiz_table
from app.auth import get_current_user
from app.auth import get_current_user

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/")
def create_quiz(quiz: Quiz, user=Depends(get_current_user)):
    if "admin" not in user.get("cognito:groups", []):
        raise HTTPException(status_code=403, detail="Only admins can create quizzes")
    
    quiz_id = str(uuid.uuid4())
    item = quiz.model_dump()
    item["quizId"] = quiz_id

    try:
        quiz_table.put_item(Item = item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"success": True, "quizId": quiz_id}