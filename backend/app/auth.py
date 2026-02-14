from fastapi import Header
import os

USE_LOCAL_AUTH = os.getenv("USE_LOCAL_AUTH", "true").lower() == "true"

def get_current_user_mock(x_user_id: str = Header(None, description="User ID")):
    if not x_user_id:
        return None
    return {"sub": x_user_id}

def get_current_user_alb(x_auth_user: str = Header(None, description="User ID")):
    if not x_auth_user:
        return None
    return {"sub": x_auth_user}

_current_user_func = get_current_user_mock if USE_LOCAL_AUTH else get_current_user_alb

get_user_dep = _current_user_func