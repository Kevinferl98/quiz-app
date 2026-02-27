import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

@pytest.fixture
def client_with_mocks():
    with patch("app.api.routes_ws.redis_client") as mock_redis, \
         patch("app.api.routes_ws.room_manager") as mock_manager, \
         patch("app.api.routes_ws.get_current_user") as mock_get_user:

        mock_redis.get_room_meta = AsyncMock()
        mock_redis.add_player = AsyncMock()
        mock_redis.get_players = AsyncMock(return_value=[])
        mock_redis.save_answer = AsyncMock()
        mock_redis.remove_player = AsyncMock()

        async def connect_side_effect(room_id, websocket):
            await websocket.accept()

        mock_manager.connect = AsyncMock(side_effect=connect_side_effect)
        mock_manager.disconnect = AsyncMock()
        mock_manager.broadcast = AsyncMock()
        mock_manager.start_quiz = AsyncMock()

        from app.main import app
        client = TestClient(app)

        yield client, mock_redis, mock_manager, mock_get_user

def test_host_can_start_quiz(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.return_value = {
        "sub": "host_user",
        "preferred_username": "Host"
    }

    mock_redis.get_room_meta.return_value = {"owner_id": "host_user"}

    with client.websocket_connect("/ws/rooms/room123?token=fake") as websocket:
        websocket.send_json({"type": "start"})

    mock_manager.start_quiz.assert_awaited_once_with("room123")

def test_player_cannot_start_quiz(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.return_value = {
        "sub": "player_1",
        "preferred_username": "John"
    }

    mock_redis.get_room_meta.return_value = {"owner_id": "host_user"}

    with client.websocket_connect("/ws/rooms/room123?token=fake") as websocket:
        websocket.send_json({"type": "start"})
        websocket.receive_json()
        data = websocket.receive_json()

        assert data["type"] == "error"
        assert "Only host" in data["message"]

    mock_manager.start_quiz.assert_not_called()

def test_player_can_join(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.side_effect = Exception()

    mock_redis.get_room_meta.return_value = {"owner_id": "host_user"}
    mock_redis.get_players.return_value = [{"name": "John"}]

    with client.websocket_connect("/ws/rooms/room123") as websocket:
        websocket.send_json({"type": "join", "name": "John"})

    mock_redis.add_player.assert_awaited_once()

    broadcast_calls = [
        args[1] for args, kwargs in mock_manager.broadcast.await_args_list
        if args[1]["type"] == "player_joined"
    ]

    assert len(broadcast_calls) >= 1
    assert "John" in broadcast_calls[-1]["players"]

def test_player_can_submit_answer(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.return_value = {
        "sub": "player_456",
        "preferred_username": "John"
    }

    mock_redis.get_room_meta.return_value = {
        "owner_id": "host_user",
        "current_question_index": 3
    }

    with client.websocket_connect("/ws/rooms/room123?token=fake") as websocket:
        websocket.send_json({"type": "answer", "answer": "C"})

    mock_redis.save_answer.assert_awaited_once_with(
        "room123",
        3,
        "player_456",
        "C"
    )

def test_unknown_action_returns_error(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.return_value = {
        "sub": "host_user",
        "preferred_username": "Host"
    }

    mock_redis.get_room_meta.return_value = {"owner_id": "host_user"}

    with client.websocket_connect("/ws/rooms/room123?token=fake") as websocket:
        websocket.send_json({"type": "invalid_action"})
        websocket.receive_json()
        data = websocket.receive_json()

        assert data["type"] == "error"
        assert data["message"] == "Unknown action"

def test_room_not_found_closes_connection(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.side_effect = Exception()
    mock_redis.get_room_meta.return_value = None

    with client.websocket_connect("/ws/rooms/room123") as websocket:
        data = websocket.receive_json()

        assert data["type"] == "error"
        assert data["message"] == "Room not found"

def test_player_disconnect_triggers_cleanup(client_with_mocks):
    client, mock_redis, mock_manager, mock_get_user = client_with_mocks

    mock_get_user.return_value = {
        "sub": "player_1",
        "preferred_username": "John"
    }

    mock_redis.get_room_meta.return_value = {"owner_id": "host_user"}
    mock_redis.get_players.return_value = []

    with client.websocket_connect("/ws/rooms/room123?token=fake") as websocket:
        websocket.close()

    mock_redis.remove_player.assert_awaited_once_with("room123", "player_1")
    mock_manager.broadcast.assert_awaited()
    mock_manager.disconnect.assert_awaited()