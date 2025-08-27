from fastapi import Header, HTTPException
import os
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv

load_dotenv()

COGNITO_POOL_ID = os.getenv("COGNITO_POOL_ID")
APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
AWS_REGION = os.getenv("AWS_REGION")

jwks_client = PyJWKClient(f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json")

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token missing")

    token = authorization.replace("Bearer ", "")

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            issuer=f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_POOL_ID}",
            algorithms=["RS256"],
            audience=COGNITO_POOL_ID,
            options={
                "verify_exp": True,
                "verify_iss": True
            }
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")