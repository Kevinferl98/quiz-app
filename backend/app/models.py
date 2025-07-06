from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option: str

class Quiz(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[Question]

class AnswerSubmission(BaseModel):
    answers: Dict[str, str]
