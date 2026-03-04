import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.room_manager import RoomManager, QUIZ_LOCK_TTL

@pytest.fixture
def redis_mock():
    redis = AsyncMock()
    redis.acquire_lock.return_value = True
    redis.release_lock.return_value = True
    redis.get_room_meta.return_value = {
        "owner_id": "owner1",
        "quiz_id": "quiz1",
        "started": False,
        "current_question_index": 0
    }
    redis.get_all_questions.return_value = [
        {"question": "Q1", "correct_option": "A"},
        {"question": "Q2", "correct_option": "B"}
    ]
    redis.get_answers.return_value = {}
    redis.get_players.return_value = [{"player_id": "p1", "name": "user", "score": 0}]
    redis.publish_room_message.return_value = None
    redis.save_room_meta.return_value = None
    redis.increment_score.return_value = None
    redis.delete_answers.return_value = None
    return redis

@pytest.fixture
def room_manager(redis_mock):
    return RoomManager(redis_mock)

@pytest.fixture(autouse=True)
def patch_durations():
    with patch("app.room_manager.QUESTION_DURATION", 0), \
         patch("app.room_manager.LEADERBOARD_DURATION", 0):
        yield

@pytest.mark.asyncio
async def test_connect_disconnect(room_manager):
    ws = AsyncMock()
    await room_manager.connect("room1", ws)
    ws.accept.assert_awaited_once()
    assert "room1" in room_manager._room_connections
    assert ws in room_manager._room_connections["room1"]

    await room_manager.disconnect("room1", ws)
    assert "room1" not in room_manager._room_connections

@pytest.mark.asyncio
async def test_broadcast_local(room_manager):
    ws1 = AsyncMock()
    ws2 = AsyncMock()
    await room_manager.connect("room1", ws1)
    await room_manager.connect("room1", ws2)

    message = {"type": "test"}
    await room_manager._broadcast_local("room1", message)

    ws1.send_json.assert_awaited_with(message)
    ws2.send_json.assert_awaited_with(message)

@pytest.mark.asyncio
async def test_start_quiz_creates_task_and_acquires_lock(room_manager, redis_mock):
    await room_manager.start_quiz("room1")
    assert "room1" in room_manager._quiz_tasks
    redis_mock.acquire_lock.assert_called_once_with("quiz_lock:room1", QUIZ_LOCK_TTL)

@pytest.mark.asyncio
async def test_start_quiz_prevents_duplicate_same_instance(room_manager, redis_mock):
    await room_manager.start_quiz("room1")
    await room_manager.start_quiz("room1")

    assert len(room_manager._quiz_tasks) == 1
    assert redis_mock.acquire_lock.call_count == 2
    redis_mock.release_lock.assert_called()

@pytest.mark.asyncio
async def test_run_quiz_publishes_question_and_leaderboard(room_manager, redis_mock):
    await room_manager.start_quiz("room1")

    tasks = list(room_manager._quiz_tasks.values())
    assert len(tasks) == 1
    await asyncio.gather(*tasks, return_exceptions=True)

    calls = redis_mock.publish_room_message.await_args_list
    question_calls = [c for c in calls if c[0][1].get("type") == "question"]
    leaderboard_calls = [c for c in calls if c[0][1].get("type") == "leaderboard"]
    assert len(question_calls) == 2
    assert len(leaderboard_calls) == 2

@pytest.mark.asyncio
async def test_cleanup_room_cancels_task(room_manager, redis_mock):
    ws = AsyncMock()
    await room_manager.connect("room1", ws)

    task = asyncio.create_task(asyncio.sleep(0.1))
    room_manager._quiz_tasks["room1"] = task

    await room_manager.disconnect("room1", ws)

    assert "room1" not in room_manager._quiz_tasks
    assert task.cancelled() or task.done()