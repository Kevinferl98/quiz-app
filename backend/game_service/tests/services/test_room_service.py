import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.room_service import create_room, ROOM_COUNTER_KEY

@pytest.fixture
def mock_redis():
    redis = MagicMock()
    redis.incr_counter = AsyncMock(return_value=42)
    redis.save_room_meta = AsyncMock()
    redis.save_questions = AsyncMock()
    return redis

@pytest.mark.asyncio
async def test_create_room_success(mock_redis):
    quiz_data = {
        "questions": [{"q": "test"}]
    }

    result = await create_room(
        redis=mock_redis,
        quiz_id="quiz1",
        user_id="user1",
        quiz_data=quiz_data
    )

    mock_redis.incr_counter.assert_called_once_with(ROOM_COUNTER_KEY)

    assert result["room_id"] == "00042"

    mock_redis.save_room_meta.assert_called_once_with(
        room_id="00042",
        owner_id="user1",
        quiz_id="quiz1",
        started=False,
        current_question_index=0,
        ttl_seconds=3600
    )

    mock_redis.save_questions.assert_called_once_with(
        room_id="00042",
        questions=[{"q": "test"}],
        ttl_seconds=3600
    )

@pytest.mark.asyncio
async def test_create_room_without_questions(mock_redis):
    quiz_data = {}

    result = await create_room(
        redis=mock_redis,
        quiz_id="quiz1",
        user_id="user1",
        quiz_data=quiz_data
    )

    mock_redis.save_questions.assert_called_once_with(
        room_id="00042",
        questions=[],
        ttl_seconds=3600
    )

    assert result["room_id"] == "00042"

@pytest.mark.asyncio
async def test_all_redis_methods_are_called(mock_redis):
    await create_room(
        redis=mock_redis,
        quiz_id="quiz1",
        user_id="user1",
        quiz_data={}
    )

    assert mock_redis.incr_counter.await_count == 1
    assert mock_redis.save_room_meta.await_count == 1
    assert mock_redis.save_questions.await_count == 1