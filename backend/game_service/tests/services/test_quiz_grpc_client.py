import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.quiz_grpc_client import get_quiz_by_id

@pytest.mark.asyncio
@patch("app.services.quiz_grpc_client.quiz_service_pb2_grpc.QuizServiceStub")
@patch("app.services.quiz_grpc_client.grpc.aio.insecure_channel")
async def test_get_quiz_by_id_success(mock_channel, mock_stub_class):
    mock_channel_instance = MagicMock()
    mock_channel.return_value.__aenter__.return_value = mock_channel_instance

    mock_stub = MagicMock()
    mock_stub_class.return_value = mock_stub

    mock_question = MagicMock()
    mock_question.id = "q1"
    mock_question.question_text = "What?"
    mock_question.options = ["A", "B"]
    mock_question.correct_option = 1

    mock_response = MagicMock()
    mock_response.quizId = "quiz1"
    mock_response.title = "Test Quiz"
    mock_response.questions = [mock_question]

    mock_stub.GetQuizById = AsyncMock(return_value=mock_response)

    result = await get_quiz_by_id("quiz1")

    assert result == {
        "quizId": "quiz1",
        "title": "Test Quiz",
        "questions": [
            {
                "id": "q1",
                "question_text": "What?",
                "options": ["A", "B"],
                "correct_option": 1,
            }
        ]
    }

    mock_stub.GetQuizById.assert_called_once()

@pytest.mark.asyncio
@patch("app.services.quiz_grpc_client.quiz_service_pb2_grpc.QuizServiceStub")
@patch("app.services.quiz_grpc_client.grpc.aio.insecure_channel")
async def test_get_quiz_grpc_error(
    mock_channel,
    mock_stub_class,
):
    mock_channel.return_value.__aenter__.return_value = MagicMock()

    mock_stub = MagicMock()
    mock_stub_class.return_value = mock_stub

    mock_stub.GetQuizById = AsyncMock(side_effect=Exception("gRPC failure"))

    with pytest.raises(Exception):
        await get_quiz_by_id("quiz1")