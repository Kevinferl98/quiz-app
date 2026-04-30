from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.middleware import logging_middleware
from app.middleware.logging_middleware import (
    _decode_body,
    _sanitize_headers,
    _truncate_text,
    setup_http_logging,
)

def _build_test_app():
    app = FastAPI()
    setup_http_logging(app)

    @app.get("/ok")
    async def ok():
        return {"status": "ok"}

    @app.post("/echo")
    async def echo(payload: dict):
        return payload

    @app.get("/boom")
    async def boom():
        raise RuntimeError("boom")

    return app


def test_sanitize_headers_redacts_sensitive():
    headers = {
        "Authorization": "Bearer abc",
        "User-Agent": "pytest",
        "X-Request-Id": "id-1",
    }
    sanitized = _sanitize_headers(headers, {"user-agent", "authorization", "x-request-id"})

    assert sanitized["authorization"] == "[REDACTED]"
    assert sanitized["user-agent"] == "pytest"
    assert sanitized["x-request-id"] == "id-1"

def test_truncate_text_marks_when_truncated():
    text, truncated = _truncate_text("abcdef", max_bytes=3)
    assert truncated is True
    assert text == "abc"

def test_decode_body_for_binary_payload():
    body, truncated = _decode_body(b"\x89PNG", "application/octet-stream", 1024)
    assert body == "[BINARY:4 bytes]"
    assert truncated is False

def test_http_logging_without_bodies(caplog, monkeypatch):
    caplog.set_level("INFO", logger="app.middleware.logging")
    monkeypatch.setattr(logging_middleware.config, "HTTP_LOG_BODIES", False)
    app = _build_test_app()
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/ok")

    assert response.status_code == 200
    assert "x-request-id" in response.headers
    messages = [r.message for r in caplog.records if r.name == "app.middleware.logging"]
    assert "http_request" in messages
    record = next(r for r in caplog.records if r.name == "app.middleware.logging" and r.message == "http_request")
    assert record.status_code == 200
    assert record.path == "/ok"

def test_http_logging_with_bodies(caplog, monkeypatch):
    caplog.set_level("INFO", logger="app.middleware.logging")
    monkeypatch.setattr(logging_middleware.config, "HTTP_LOG_BODIES", True)
    monkeypatch.setattr(logging_middleware.config, "HTTP_LOG_MAX_BODY_BYTES", 4096)
    app = _build_test_app()
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/echo", json={"hello": "world"})

    assert response.status_code == 200
    record = next(r for r in caplog.records if r.name == "app.middleware.logging" and r.message == "http_request")
    assert record.request_body == {"hello": "world"}
    assert record.response_body == {"hello": "world"}
    assert record.request_body_truncated is False
    assert record.response_body_truncated is False

def test_http_logging_exception_path(caplog, monkeypatch):
    caplog.set_level("ERROR", logger="app.middleware.logging")
    monkeypatch.setattr(logging_middleware.config, "HTTP_LOG_BODIES", False)
    app = _build_test_app()
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/boom")

    assert response.status_code == 500
    messages = [r.message for r in caplog.records if r.name == "app.middleware.logging"]
    assert "http_request_failed" in messages