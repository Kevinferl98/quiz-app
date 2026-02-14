import pytest
from app.main import app
from app.auth import get_user_dep
from fastapi.testclient import TestClient

mock_user = {"sub": "user_123"}

@pytest.fixture(autouse=True)
def auth_overrider():
    app.dependency_overrides[get_user_dep] = lambda: mock_user
    yield
    app.dependency_overrides.clear()