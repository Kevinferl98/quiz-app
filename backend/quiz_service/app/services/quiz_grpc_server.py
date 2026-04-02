import grpc
from app.services.grpc_generated import quiz_service_pb2, quiz_service_pb2_grpc
from app.services.quiz_service import QuizService
from app.repositories.quiz_repository import QuizRepository
from app.db.mongo_client import mongo_db

class QuizServiceServicer(quiz_service_pb2_grpc.QuizServiceServicer):
    def __init__(self, quiz_service: QuizService):
        self.quiz_service = quiz_service

    async def GetQuizById(self, request, context):
        quiz_data = self.quiz_service.get_quiz_by_id(request.quizId)

        if not quiz_data:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Quiz not found")
        
        return quiz_service_pb2.Quiz(
            quizId=quiz_data["quizId"],
            title=quiz_data.get("title", ""),
            questions=[
                quiz_service_pb2.Question(
                    id=q["id"],
                    question_text=q["question_text"],
                    options=q["options"],
                    correct_option=q["correct_option"]
                )
                for q in quiz_data.get("questions", [])
            ]
        )

async def serve():
    repo = QuizRepository(mongo_db.quizzes)
    service = QuizService(repo)

    server = grpc.aio.server()
    quiz_service_pb2_grpc.add_QuizServiceServicer_to_server(
        QuizServiceServicer(quiz_service=service), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Quiz gRPC server running on port 50051")
    await server.wait_for_termination()