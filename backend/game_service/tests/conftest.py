import pytest
from app.main import app
from app.auth import get_current_user

mock_user = {"sub": "user_123"}

@pytest.fixture(autouse=True)
def auth_overrider():
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.clear()