from fastapi import Request, HTTPException
import jwt

def get_current_user(request: Request):
    """
    Recupera i dati dall'utente autenticato
    """
    token = request.headers.get("x-amzn-oidc-data")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
def is_admin(user):
    return "admin" in user.get("cognito:groups", [])