from fastapi import APIRouter, HTTPException
import uuid
from app.models import Quiz
from app.models import AnswerSubmission
from app.db.dynamodb_client import quiz_table

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/")
def list_quizzes():
    try:
        response = quiz_table.scan(ProjectionExpression="quizId, title")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    quizzes = response.get("Items", [])
    return {"quizzes": quizzes}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str):
    try:
        response = quiz_table.get_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return response["Item"]

@router.post("/")
def create_quiz(quiz: Quiz):
    quiz_id = str(uuid.uuid4())
    item = quiz.model_dump()
    item["quizId"] = quiz_id

    try:
        quiz_table.put_item(Item = item)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"success": True, "quizId": quiz_id}

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str):
    try:
        quiz_table.delete_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"success": True}

@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: str, answers: AnswerSubmission):
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = response["Item"]
    correct = 0
    total = len(quiz.get("questions", []))

    for question in quiz.get("questions", []):
        qid = question.get("id")
        if answers.answers.get(qid) == question.get("correct_option"):
            correct += 1

    return {"total": total, "correct": correct, "score_percent": correct / total * 100}