from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option: str

class Quiz(BaseModel):
    quizId: Optional[str] = None
    owner_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    questions: List[Question]
    is_public: bool = True

class AnswerSubmission(BaseModel):
    answers: Dict[str, str]
