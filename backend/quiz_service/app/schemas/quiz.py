from pydantic import BaseModel
from typing import List, Optional, Dict

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option: str

class Quiz(BaseModel):
    quizId: str
    owner_id: str
    title: str
    description: str | None = None
    questions: List[Question]
    is_public: bool = True

class QuizCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[Question]
    is_public: bool = True

class QuizCreateResponse(BaseModel):
    success: bool
    quizId: str

class QuizDeleteResponse(BaseModel):
    success: bool

class AnswerSubmission(BaseModel):
    answers: Dict[str, str]

class QuestionOut(BaseModel):
    id: str
    question_text: str
    options: List[str]

class QuizOut(BaseModel):
    quizId: str
    title: str

class QuizzesResponse(BaseModel):
    quizzes: List[QuizOut]

class QuizzesResponsePaginated(BaseModel):
    quizzes: List[QuizOut]
    total: int
    page: int
    pages: int

class AnswerRequest(BaseModel):
    question_id: str
    answer: str

class AnswerResponse(BaseModel):
    correct: bool

class QuizDetailResponse(BaseModel):
    quizId: str
    title: str
    description: str | None = None
    questions: List[QuestionOut]