import app.auth as auth

def test_get_current_user_mock_success():
    result = auth.get_current_user_mock(x_user_id="user_123")
    assert result == {"sub": "user_123"}

def test_get_current_user_mock_none():
    result = auth.get_current_user_mock(x_user_id=None)
    assert result is None

def test_get_current_user_alb_success():
    result = auth.get_current_user_alb(x_auth_user="user_456")
    assert result == {"sub": "user_456"}

def test_get_current_user_alb_none():
    result = auth.get_current_user_alb(x_auth_user=None)
    assert result is None