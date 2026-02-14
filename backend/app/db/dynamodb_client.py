import boto3
import os
from botocore.exceptions import ClientError

IS_LOCAL = os.getenv("IS_LOCAL", "false").lower() == "true"
DYNAMODB_ENDPOINT = "http://dynamodb:8000" if IS_LOCAL else None

if IS_LOCAL:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        endpoint_url=DYNAMODB_ENDPOINT,
        aws_access_key_id="fakeAccessKeyId",
        aws_secret_access_key="fakeSecretAccessKey"
    )
else:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def create_tables_if_not_exist():
    try:
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

        if "Quizzes" not in existing_tables:
            dynamodb.create_table(
                TableName="Quizzes",
                KeySchema=[{"AttributeName": "quizId", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "quizId", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST"
            )
            print("Created table 'Quizzes'")

        if "Results" not in existing_tables:
            dynamodb.create_table(
                TableName="Results",
                KeySchema=[
                    {"AttributeName": "userId", "KeyType": "HASH"},
                    {"AttributeName": "quizId", "KeyType": "RANGE"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "userId", "AttributeType": "S"},
                    {"AttributeName": "quizId", "AttributeType": "S"}
                ],
                BillingMode="PAY_PER_REQUEST"
            )
            print("Created table 'Results'")
    except ClientError as e:
        print(f"Error creating tables: {e}")

if IS_LOCAL:
    create_tables_if_not_exist()

quiz_table = dynamodb.Table("Quizzes")
results_table = dynamodb.Table("Results")