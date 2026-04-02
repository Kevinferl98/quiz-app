from fastapi import Depends
from app.repositories.quiz_repository import QuizRepository
from app.services.quiz_service import QuizService
from app.db.mongo_client import mongo_db

def get_quiz_repository() -> QuizRepository:
    return QuizRepository(mongo_db.quizzes)

def get_quiz_service(repo: QuizRepository = Depends(get_quiz_repository)) -> QuizService:
    return QuizService(repo)