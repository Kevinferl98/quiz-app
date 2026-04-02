import pytest
from unittest.mock import AsyncMock, MagicMock
import grpc
from app.services.grpc_generated import quiz_service_pb2
from app.services.quiz_grpc_server import QuizServiceServicer

@pytest.mark.asyncio
class TestQuizServiceServicer:

    @pytest.fixture
    def mock_service(self):
        return MagicMock()

    async def test_get_quiz_by_id_success(self, mock_service):
        mock_service.get_quiz_by_id.return_value = {
            "quizId": "quiz-123",
            "title": "Python Basics",
            "questions": [
                {
                    "id": "q1",
                    "question_text": "Text",
                    "options": ["A", "B"],
                    "correct_option": "A"
                }
            ]
        }

        context = AsyncMock(spec=grpc.aio.ServicerContext)
        servicer = QuizServiceServicer(quiz_service=mock_service)
        request = quiz_service_pb2.GetQuizRequest(quizId="quiz-123")

        response = await servicer.GetQuizById(request, context)

        assert response.quizId == "quiz-123"
        assert response.title == "Python Basics"
        assert len(response.questions) == 1
        assert response.questions[0].id == "q1"
        mock_service.get_quiz_by_id.assert_called_once_with("quiz-123")

    async def test_get_quiz_by_id_not_found(self, mock_service):
        mock_service.get_quiz_by_id.return_value = None
        
        servicer = QuizServiceServicer(quiz_service=mock_service)
        context = AsyncMock(spec=grpc.aio.ServicerContext)

        context.abort.side_effect = Exception("gRPC Abort")

        request = quiz_service_pb2.GetQuizRequest(quizId="non-existent")

        with pytest.raises(Exception, match="gRPC Abort"):
            await servicer.GetQuizById(request, context)

        context.abort.assert_called_once_with(
            grpc.StatusCode.NOT_FOUND,
            "Quiz not found"
        )