import pytest
from unittest.mock import AsyncMock, patch
from app.room_manager import RoomManager

@pytest.fixture
def manager():
    return RoomManager()

@pytest.fixture
def mock_ws():
    ws = AsyncMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws

@pytest.fixture
def mock_redis():
    with patch("app.room_manager.redis_client") as mock_redis:
        mock_redis.get_room_meta = AsyncMock()
        mock_redis.save_room_meta = AsyncMock()
        mock_redis.get_all_questions = AsyncMock()
        mock_redis.get_answers = AsyncMock()
        mock_redis.increment_score = AsyncMock()
        mock_redis.delete_answers = AsyncMock()
        mock_redis.get_players = AsyncMock()
        yield mock_redis

@pytest.mark.asyncio
async def test_connect_adds_websocket(manager, mock_ws):
    room_id = "room123"
    await manager.connect(room_id, mock_ws)

    assert room_id in manager.room_connections
    assert mock_ws in manager.room_connections[room_id]
    mock_ws.accept.assert_awaited_once()

@pytest.mark.asyncio
async def test_disconnect_cleans_up_room(manager, mock_ws):
    room_id = "room123"
    await manager.connect(room_id, mock_ws)

    await manager.disconnect(room_id, mock_ws)

    assert room_id not in manager.room_connections
    assert room_id not in manager.quiz_tasks

@pytest.mark.asyncio
async def test_broadcast_removes_dead_connection(manager, mock_ws):
    room_id = "room123"
    await manager.connect(room_id, mock_ws)

    mock_ws.send_json.side_effect = Exception("Connection lost")
    await manager.broadcast(room_id, {"msg": "hello"})

    assert room_id not in manager.room_connections

@pytest.mark.asyncio
async def test_start_quiz_creates_task(manager, mock_ws, mock_redis):
    room_id = "room123"
    await manager.connect(room_id, mock_ws)
    mock_redis.get_room_meta.return_value = {"owner_id": "user1", "quiz_id": "q1"}
    mock_redis.get_all_questions.return_value = []

    await manager.start_quiz(room_id)

    assert room_id in manager.quiz_tasks
    task = manager.quiz_tasks[room_id]
    assert not task.done()

@pytest.mark.asyncio
async def test_run_quiz_flow(manager, mock_ws, mock_redis):
    room_id = "test_room"
    mock_meta = {"owner_id": "user1", "quiz_id": "q1"}
    mock_question = {
        "text": "2+2?", 
        "options": ["3", "4"], 
        "correct_option": "4"
    }

    mock_redis.get_room_meta.return_value = mock_meta
    mock_redis.get_all_questions.return_value = [mock_question]
    mock_redis.get_answers.return_value = {"player1": "4"} 
    mock_redis.get_players.return_value = [{"name": "P1", "score": 10}]

    await manager.connect(room_id, mock_ws)

    with patch("app.room_manager.QUESTION_DURATION", 0), \
         patch("app.room_manager.LEADERBOARD_DURATION", 0), \
         patch("asyncio.sleep", AsyncMock()):

        await manager._run_quiz(room_id)

    calls = [call.args[0]["type"] for call in mock_ws.send_json.await_args_list]
    assert "question" in calls
    assert "leaderboard" in calls
    assert "end" in calls

    mock_redis.increment_score.assert_awaited_with(room_id, "player1")

    final_call = mock_redis.save_room_meta.await_args_list[-1][1]
    assert final_call["started"] is False
    assert final_call["current_question_index"] == 1
