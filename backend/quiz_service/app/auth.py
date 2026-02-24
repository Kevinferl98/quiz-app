from fastapi import Header, HTTPException
import os
import jwt
from jwt import PyJWKClient

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM = os.getenv("KEYCLOAK_REALM")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

jwks_client = PyJWKClient(JWKS_URL)

USE_LOCAL_AUTH = os.getenv("USE_LOCAL_AUTH", "true").lower() == "true"

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token missing")
    
    token = authorization.replace("Bearer ", "")

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=f"http://localhost:8081/realms/{REALM}",
            options={
                "verify_exp": True,
                "verify_iss": True
            }
        )

        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")