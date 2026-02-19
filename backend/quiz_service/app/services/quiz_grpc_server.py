import grpc
from app.services.grpc_generated import quiz_service_pb2, quiz_service_pb2_grpc
from app.services.quiz_service import get_quiz_by_id

class QuizServiceServicer(quiz_service_pb2_grpc.QuizServiceServicer):
    async def GetQuizById(self, request, context):
        quiz_data = get_quiz_by_id(request.quizId)

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
    server = grpc.aio.server()
    quiz_service_pb2_grpc.add_QuizServiceServicer_to_server(
        QuizServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Quiz gRPC server running on port 50051")
    await server.wait_for_termination()