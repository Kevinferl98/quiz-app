import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch("app.services.room_service.redis_client")
@patch("uuid.uuid4")
async def test_room_service_logic(mock_uuid, mock_redis):
    from app.services.room_service import create_room
    
    mock_redis.save_room_meta = AsyncMock()
    mock_redis.save_questions = AsyncMock()
    mock_redis.incr_counter = AsyncMock(return_value=12345)
    
    quiz_data = {
        "quizId": "q1",
        "title": "T",
        "questions": [{"id": "1", "question_text": "Q", "options": ["A"], "correct_option": "A"}]
    }
    
    result = await create_room("q1", "user_123", quiz_data)
    
    assert result == {"room_id": "12345"}
    mock_redis.save_room_meta.assert_awaited_once()
    mock_redis.save_questions.assert_awaited_once()
    mock_redis.incr_counter.assert_awaited_once_with("global_room_counter")