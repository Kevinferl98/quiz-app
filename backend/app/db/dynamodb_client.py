import boto3
import os

dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
quiz_table = dynamodb.Table("Quizzes")