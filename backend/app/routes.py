from fastapi import APIRouter, Depends, HTTPException
import uuid
from app.models import Quiz
from app.models import AnswerSubmission
from app.db.dynamodb_client import quiz_table, results_table
from app.auth import get_current_user
from decimal import Decimal

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/public")
def list_public_quizzes():
    try:
        response = quiz_table.scan(
            FilterExpression="is_public = :val",
            ExpressionAttributeValues={":val": True},
            ProjectionExpression="quizId, title"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"quizzes": response.get("Items", [])}

@router.get("/mine")
def list_my_quizzes(user=Depends(get_current_user())):
    if not user:
        raise HTTPException(status_code=403, detail="Login required")
    
    try:
        response = quiz_table.scan(
            FilterExpression="owner_id = :owner_id",
            ExpressionAttributeValues={":owner_id": user["sub"]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"quizzes": response.get("Items", [])}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str, user=Depends(get_current_user())):
    try:
        response = quiz_table.get_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return response["Item"]

@router.post("/")
def create_quiz(quiz: Quiz, user=Depends(get_current_user())):    
    if user is None:
        raise HTTPException(status_code=401, detail="User not logged in")
    quiz_id = str(uuid.uuid4())
    item = quiz.model_dump()
    item["quizId"] = quiz_id
    item["owner_id"] = user["sub"]

    try:
        quiz_table.put_item(Item = item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"success": True, "quizId": quiz_id}

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str, user=Depends(get_current_user())):
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if response["Item"]["owner_id"] != user["sub"]:
        raise HTTPException(status_code=403, detail="You can only delete your own quizzes")

    try:
        quiz_table.delete_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"success": True}

@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: str, answers: AnswerSubmission, user=Depends(get_current_user)):
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = response["Item"]
    correct = 0
    total = len(quiz.get("questions", []))

    for question in quiz.get("questions", []):
        qid = question.get("id")
        if answers.get(qid) == question.get("correct_option"):
            correct += 1
    score_percent = correct / total * 100 if total > 0 else 0

    result_item = {
        "userId": user["sub"],
        "quizId": quiz_id,
        "quizTitle": quiz.get("title", ""),
        "score_percent":  Decimal(str(score_percent)),
        "correct": correct,
        "total": total
    }

    try:
        results_table.put_item(Item=result_item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"total": total, "correct": correct, "score_percent": score_percent}