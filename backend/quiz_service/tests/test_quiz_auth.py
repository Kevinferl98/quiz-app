import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from app.auth import get_current_user
import jwt

def test_get_current_user_missing_bearer():
    with pytest.raises(HTTPException) as exc:
        get_current_user("InvalidFormat token123")
    assert exc.value.status_code == 401
    assert exc.value.detail == "Bearer token missing"

@patch("app.auth.jwks_client.get_signing_key_from_jwt")
@patch("jwt.decode")
def test_get_current_user_success(mock_jwt_decode, mock_get_key):
    mock_key = MagicMock()
    mock_key.key = "fake-public-key"
    mock_get_key.return_value = mock_key
    
    expected_payload = {
        "sub": "user_123",
        "email": "test@example.com",
        "preferred_username": "john.doe"
    }
    mock_jwt_decode.return_value = expected_payload

    result = get_current_user("Bearer fake-token-123")

    assert result == expected_payload
    mock_jwt_decode.assert_called_once()    

@patch("app.auth.jwks_client.get_signing_key_from_jwt")
def test_get_current_user_jwks_error(mock_get_key):
    mock_get_key.side_effect = Exception("JWKS endpoint unreachable")
    
    with pytest.raises(HTTPException) as exc:
        get_current_user("Bearer some-token")
    
    assert exc.value.status_code == 401
    assert "Invalid token" in exc.value.detail

@patch("app.auth.jwks_client.get_signing_key_from_jwt")
@patch("jwt.decode")
def test_get_current_user_expired_token(mock_jwt_decode, mock_get_key):
    mock_get_key.return_value = MagicMock(key="fake-key")
    
    mock_jwt_decode.side_effect = jwt.ExpiredSignatureError("Token expired")
    
    with pytest.raises(HTTPException) as exc:
        get_current_user("Bearer expired-token")
    
    assert exc.value.status_code == 401
    assert "Token expired" in exc.value.detail