from app.db.dynamodb_client import quiz_table, results_table
from decimal import Decimal
import uuid

def list_public_quizzes():
    response = quiz_table.scan(
        FilterExpression="is_public = :val",
        ExpressionAttributeValues={":val": True},
        ProjectionExpression="quizId, title"
    )
    return response.get("Items", [])

def list_personal_quizzes(owner_id: str):
    response = quiz_table.scan(
        FilterExpression="owner_id = :owner_id",
        ExpressionAttributeValues={":owner_id": owner_id}
    )

    return response.get("Items", [])

def get_quiz_by_id(quiz_id: str):
    response = quiz_table.get_item(Key={"quizId": quiz_id})
    return response.get("Item")

def create_quiz(quiz_data: dict, owner_id: str):
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


def submit_quiz(quiz_id: str, answers: dict, user_id: str) -> dict:
    response = quiz_table.get_item(Key={"quizId": quiz_id})

    if "Item" not in response:
        raise ValueError("Quiz not found")

    quiz = response["Item"]
    questions = quiz.get("questions", [])
    total = len(questions)

    correct = 0
    for question in questions:
        qid = question.get("id")
        if answers.get(qid) == question.get("correct_option"):
            correct += 1

    score_percent = correct / total * 100 if total > 0 else 0

    result_item = {
        "userId": user_id,
        "quizId": quiz_id,
        "quizTitle": quiz.get("title", ""),
        "score_percent": Decimal(str(score_percent)),
        "correct": correct,
        "total": total
    }

    results_table.put_item(Item=result_item)

    return {
        "total": total,
        "correct": correct,
        "score_percent": score_percent
    }