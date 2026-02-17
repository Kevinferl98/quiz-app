from fastapi import APIRouter, Depends, HTTPException
from app.services import room_service
from app.auth import get_user_dep
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/{quiz_id}/create_room")
async def create_room(quiz_id: str, user=Depends(get_user_dep)):
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    
    quiz_data = quiz_service.get_quiz_by_id(quiz_id)
    if not quiz_data:
        logger.warning(f"Quiz {quiz_id} not found")
        raise HTTPException(status_code=404, detail="Quiz not found")

    return await room_service.create_room(quiz_id, user["sub"], quiz_data)