from pymongo.collection import Collection
from typing import Dict, Any

class QuizRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_public_quizzes(self) -> list[Dict[str, Any]]:
        return list(self.collection.find(
            {"is_public": True},
            {"quizId": 1, "title": 1, "_id": 0}
        ))

    def find_by_owner(self, owner_id: str) -> list[Dict[str, Any]]:
        return list(self.collection.find(
            {"owner_id": owner_id}
        ))

    def find_by_id(self, quiz_id: str) -> Dict[str, Any] | None:
        return self.collection.find_one({"quizId": quiz_id})

    def insert(self, quiz: dict) -> None:
        self.collection.insert_one(quiz)

    def delete(self, quiz_id: str) -> None:
        self.collection.delete_one({"quizId": quiz_id})
