from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.quiz import Question

class Player(BaseModel):
    player_id: str
    name: str
    score: int = 0
    current_answer: Optional[str] = None

class Room(BaseModel):
    room_id: str
    quiz_id: str
    owner_id: str
    players: List[Player] = Field(default_factory=list)
    started: bool = False
    current_question_index: int = 0
    question_timer: Optional[int] = None
    questions: List[Question] = Field(default_factory=list)
    show_leaderboard: bool = False