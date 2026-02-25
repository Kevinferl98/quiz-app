from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option: str

class Quiz(BaseModel):
    quizId: Optional[str] = Field(None, exclude=True)
    owner_id: Optional[str] = Field(None, exclude=True)
    title: str
    description: Optional[str] = None
    questions: List[Question]
    is_public: bool = True

class AnswerSubmission(BaseModel):
    answers: Dict[str, str]

class QuestionOut(BaseModel):
    id: str
    question_text: str
    options: List[str]

class QuizOut(BaseModel):
    quizId: str
    title: str
    questions: List[QuestionOut]

class AnswerRequest(BaseModel):
    question_id: str
    answer: str

class AnswerResponse(BaseModel):
    correct: bool