import json, boto3, decimal

def lambda_handler(event, context):
    claims = event["requestContext"]["authorizer"]["claims"]
    user_id = claims["sub"]

    body = json.loads(event["body"])
    quiz_id = body["quizId"]
    answers = body["answers"]

    dynamodb = boto3.resource("dynamodb")
    quiz_table = dynamodb.Table("quiz_table")
    results_table = dynamodb.Table("results_table")

    resp = quiz_table.get_item(Key={"quizId": quiz_id})
    if "Item" not in resp:
        return {"statusCode": 404, "body": json.dumps({"error": "Quiz not found"})}

    quiz = resp["Item"]
    correct = 0
    total = len(quiz.get("questions", []))

    for question in quiz.get("questions", []):
        qid = question.get("id")
        if answers.get(qid) == question.get("correct_option"):
            correct += 1

    score_percent = correct / total * 100 if total > 0 else 0

    result_item = {
        "userId": user_id,
        "quizId": quiz_id,
        "quizTitle": quiz.get("title", ""),
        "score_percent": decimal.Decimal(str(score_percent)),
        "correct": correct,
        "total": total
    }

    results_table.put_item(Item=result_item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "total": total,
            "correct": correct,
            "score_percent": score_percent
        })
    }