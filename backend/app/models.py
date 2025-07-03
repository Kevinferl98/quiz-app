from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option: str

class Quiz(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[Question]
