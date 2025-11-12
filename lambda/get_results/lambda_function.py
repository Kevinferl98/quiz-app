import json, boto3

def lambda_handler(event, context):
    claims = event["requestContext"]["authorizer"]["claims"]
    user_id = claims["sub"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("results_table")

    resp = table.query(
        KeyConditionExpression="userId = :uid",
        ExpressionAttributeValues={":uid": user_id}
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp["Items"], default=str)
    }