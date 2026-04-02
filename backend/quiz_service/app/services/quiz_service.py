import uuid
from app.schemas.quiz import Quiz, QuizCreateRequest
from app.repositories.quiz_repository import QuizRepository
from typing import Dict, Any

class QuizService:
    def __init__(self, repo: QuizRepository) -> None:
        self.repo = repo

    def list_public_quizzes(self) -> list[Dict[str, Any]]:
        return self.repo.find_public_quizzes()

    def list_personal_quizzes(self, owner_id: str) -> list[Dict[str, Any]]:
        return self.repo.find_by_owner(owner_id)

    def get_quiz_by_id(self, quiz_id: str) -> Dict[str, Any] | None:
        return self.repo.find_by_id(quiz_id)

    def create_quiz(self, quiz_data: QuizCreateRequest, owner_id: str) -> str:
        quiz_id = str(uuid.uuid4())

        quiz = Quiz(
            quizId=quiz_id,
            owner_id=owner_id,
            **quiz_data.model_dump()
        )

        self.repo.insert(quiz.model_dump())
        return quiz_id

    def delete_quiz(self, quiz_id: str, user_id: str) -> None:
        quiz = self.repo.find_by_id(quiz_id)

        if not quiz:
            raise ValueError("Quiz not found")

        if quiz["owner_id"] != user_id:
            raise PermissionError("Not owner")

        self.repo.delete(quiz_id)

    def check_answer(self, quiz_id: str, question_id: str, answer: str) -> bool:
        quiz = self.repo.find_by_id(quiz_id)

        if not quiz:
            raise ValueError("Quiz not found")

        question = next(
            (q for q in quiz.get("questions", []) if q.get("id") == question_id),
            None
        )

        if not question:
            raise ValueError("Question not found in quiz")

        return question.get("correct_option") == answer