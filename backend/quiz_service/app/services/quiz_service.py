from app.db.dynamodb_client import quiz_table, results_table
from decimal import Decimal
from typing import Dict, Any
import uuid

def list_public_quizzes() -> list[Dict[str, Any]]:
    response = quiz_table.scan(
        FilterExpression="is_public = :val",
        ExpressionAttributeValues={":val": True},
        ProjectionExpression="quizId, title"
    )
    return response.get("Items", [])

def list_personal_quizzes(owner_id: str) -> list[Dict[str, Any]]:
    response = quiz_table.scan(
        FilterExpression="owner_id = :owner_id",
        ExpressionAttributeValues={":owner_id": owner_id}
    )

    return response.get("Items", [])

def get_quiz_by_id(quiz_id: str) -> Dict[str, Any] | None:
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    return response.get("Item")

def create_quiz(quiz_data: dict, owner_id: str)  -> str:
    quiz_id = str(uuid.uuid4())
    quiz_data["quizId"] = quiz_id
    quiz_data["owner_id"] = owner_id
    quiz_table.put_item(Item=quiz_data)
    return quiz_id

def delete_quiz(quiz_id: str, user_id: str) -> None:
    response = quiz_table.get_item(Key={"quizId": quiz_id})

    if "Item" not in response:
        raise ValueError("Quiz not found")

    if response["Item"]["owner_id"] != user_id:
        raise PermissionError("Not owner")

    quiz_table.delete_item(Key={"quizId": quiz_id})

def check_answer(quiz_id: str, question_id: str, answer: str) -> bool:
    quiz = get_quiz_by_id(quiz_id)

    if not quiz:
        raise ValueError("Quiz not found")
    
    question = next((q for q in quiz.get("questions", []) if q.get("id") == question_id), None)
    if not question:
        raise ValueError("Question not found in quiz")
    
    return question.get("correct_option") == answer