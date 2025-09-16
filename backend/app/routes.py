from fastapi import APIRouter, Depends, HTTPException
import uuid
from app.models import Quiz
from app.models import Question
from app.models import AnswerSubmission
from app.db.dynamodb_client import quiz_table, results_table
from app.auth import get_current_user
from decimal import Decimal

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/")
def list_quizzes(user=Depends(get_current_user)):
    try:
        response = quiz_table.scan(ProjectionExpression="quizId, title")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    quizzes = response.get("Items", [])
    return {"quizzes": quizzes}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str, user=Depends(get_current_user)):
    try:
        response = quiz_table.get_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return response["Item"]

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

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: str, user=Depends(get_current_user)):
    if "admin" not in user.get("cognito:groups", []):
        raise HTTPException(status_code=403, detail="Only admins can delete quizzes")

    try:
        quiz_table.delete_item(Key={"quizId": quiz_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"success": True}

@router.delete("/{quiz_id}/questions/{question_id}")
def delete_question(quiz_id: str, question_id: str, user=Depends(get_current_user)):
    if "admin" not in user.get("cognito:groups", []):
        raise HTTPException(status_code=403, detail="Only admins can delete a questions")
    
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = response["Item"]
    quiz["questions"] = [q for q in quiz.get("questions", []) if q.get("id") != question_id]

    try:
        quiz_table.put_item(Item=quiz)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {"success": True}

@router.post("/{quiz_id}/questions")
def add_question(quiz_id: str, question: Question, user=Depends(get_current_user)):
    if "admin" not in user.get("cognito:groups", []):
        raise HTTPException(status_code=403, detail="Only admins can add questions")

    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = response["Item"]
    quiz.setdefault("questions", []).append(question.model_dump())

    try:
        quiz_table.put_item(Item=quiz)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return {"success": True}

@router.patch("/{quiz_id}/questions/{question_id}")
def update_question(quiz_id: str, question_id: str, updates: dict, user=Depends(get_current_user)):
    if "admin" not in user.get("cognito:groups", []):
        raise HTTPException(status_code=403, detail="Only admin can modify questions")
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = response["Item"]
    updated = False
    for q in quiz.get("questions", []):
        if q.get("id") == question_id:
            q.update(updates)
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    
    try:
        quiz_table.put_item(Item=quiz)
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