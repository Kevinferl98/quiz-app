import grpc
from app.services.grpc_generated import quiz_service_pb2, quiz_service_pb2_grpc

QUIZ_SERVICE_HOST = "quiz_service:50051"

async def get_quiz_by_id(quiz_id: str) -> dict:
    async with grpc.aio.insecure_channel(QUIZ_SERVICE_HOST) as channel:
        stub = quiz_service_pb2_grpc.QuizServiceStub(channel)

        response = await stub.GetQuizById(
            quiz_service_pb2.GetQuizRequest(quizId=quiz_id)
        )

        return {
            "quizId": response.quizId,
            "title": response.title,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "options": list(q.options),
                    "correct_option": q.correct_option,
                }
                for q in response.questions
            ]
        }