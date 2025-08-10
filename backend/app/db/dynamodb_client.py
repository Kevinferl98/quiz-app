import boto3
import os

IS_LOCAL = os.getenv("IS_LOCAL", "false").lower() == "true"

if IS_LOCAL:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="", 
        endpoint_url="http://localhost:8000",
        aws_access_key_id="",
        aws_secret_access_key=""
        )
else:
    dynamodb = boto3.resource("dynamodb", region_name="")

quiz_table = dynamodb.Table("Quizzes")
results_table = dynamodb.Table("Results")