from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from typing import Dict, Any
from app.exception import DatabaseError

class QuizRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_public_quizzes(self) -> list[Dict[str, Any]]:
        try:
            return list(self.collection.find(
                {"is_public": True},
                {"quizId": 1, "title": 1, "_id": 0}
            ))
        except PyMongoError as e:
            raise DatabaseError("Error fetching public quizzes") from e

    def find_by_owner(self, owner_id: str) -> list[Dict[str, Any]]:
        try:
            return list(self.collection.find({"ownerId": owner_id}))
        except PyMongoError as e:
            raise DatabaseError("Error fetching user quizzes") from e

    def find_by_id(self, quiz_id: str) -> Dict[str, Any] | None:
        try:
            return self.collection.find_one({"quizId": quiz_id})
        except PyMongoError as e:
            raise DatabaseError("Error fetching quiz") from e

    def insert(self, quiz: dict) -> None:
        try:
            self.collection.insert_one(quiz)
        except PyMongoError as e:
            raise DatabaseError("Error inserting quiz") from e

    def delete(self, quiz_id: str) -> None:
        try:
            self.collection.delete_one({"quizId": quiz_id})
        except PyMongoError as e:
            raise DatabaseError("Error deleting quiz") from e
