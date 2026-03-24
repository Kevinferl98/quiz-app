import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.room_service import create_room

@pytest.fixture
def mock_redis():
    redis = MagicMock()
    redis.set_if_not_exists = AsyncMock(return_value=True)
    redis.save_room_meta = AsyncMock()
    redis.save_questions = AsyncMock()
    return redis

@pytest.mark.asyncio
async def test_create_room_success(mock_redis):
    quiz_data = {
        "questions": [{"q": "test"}]
    }

    with patch("app.services.room_service.generate_room_code", return_value="ABCDE"):
        result = await create_room(
            redis=mock_redis,
            quiz_id="quiz1",
            user_id="user1",
            quiz_data=quiz_data
        )

    mock_redis.set_if_not_exists.assert_called_once_with(
        key="room:ABCDE:lock",
        value="1",
        ttl=3600
    )

    assert result["room_id"] == "ABCDE"

    mock_redis.save_room_meta.assert_called_once_with(
        room_id="ABCDE",
        owner_id="user1",
        quiz_id="quiz1",
        started=False,
        current_question_index=0,
        ttl_seconds=3600
    )

    mock_redis.save_questions.assert_called_once_with(
        room_id="ABCDE",
        questions=[{"q": "test"}],
        ttl_seconds=3600
    )

@pytest.mark.asyncio
async def test_create_room_without_questions(mock_redis):
    quiz_data = {}

    with patch("app.services.room_service.generate_room_code", return_value="ABCDE"):
        result = await create_room(
            redis=mock_redis,
            quiz_id="quiz1",
            user_id="user1",
            quiz_data=quiz_data
        )

    mock_redis.save_questions.assert_called_once_with(
        room_id="ABCDE",
        questions=[],
        ttl_seconds=3600
    )

    assert result["room_id"] == "ABCDE"

@pytest.mark.asyncio
async def test_all_redis_methods_are_called(mock_redis):
    with patch("app.services.room_service.generate_room_code", return_value="ABCDE"):
        await create_room(
            redis=mock_redis,
            quiz_id="quiz1",
            user_id="user1",
            quiz_data={}
        )

    assert mock_redis.set_if_not_exists.await_count == 1
    assert mock_redis.save_room_meta.await_count == 1
    assert mock_redis.save_questions.await_count == 1