import pytest
from unittest.mock import patch, AsyncMock
import grpc
from app.services.grpc_generated import quiz_service_pb2
from app.services.quiz_grpc_server import QuizServiceServicer

@pytest.mark.asyncio
class TestQuizServiceServicer:

    @patch("app.services.quiz_service.quiz_table.get_item")
    async def test_get_quiz_by_id_success(self, mock_get_item):
        mock_get_item.return_value = {
            "Item": {
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
        }

        context = AsyncMock(spec=grpc.aio.ServicerContext)
        servicer = QuizServiceServicer()
        request = quiz_service_pb2.GetQuizRequest(quizId="quiz-123")

        response = await servicer.GetQuizById(request, context)

        assert response.quizId == "quiz-123"
        assert response.title == "Python Basics"
        assert response.questions[0].id == "q1"
        mock_get_item.assert_called_once()

    @patch("app.services.quiz_service.quiz_table.get_item")
    async def test_get_quiz_by_id_not_found(self, mock_get_item):
        mock_get_item.return_value = {}

        context = AsyncMock(spec=grpc.aio.ServicerContext)
        context.abort.side_effect = grpc.RpcError("Not Found")
        
        servicer = QuizServiceServicer()
        request = quiz_service_pb2.GetQuizRequest(quizId="non-existent")

        with pytest.raises(grpc.RpcError):
            await servicer.GetQuizById(request, context)
        
        context.abort.assert_called_once_with(
            grpc.StatusCode.NOT_FOUND, 
            "Quiz not found"
        )