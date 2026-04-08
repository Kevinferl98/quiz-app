import pytest
from unittest.mock import MagicMock
from pymongo.errors import PyMongoError
from app.exception import DatabaseError
from app.repositories.quiz_repository import QuizRepository

@pytest.fixture
def mock_collection():
    return MagicMock()

@pytest.fixture
def repository(mock_collection):
    return QuizRepository(mock_collection)

def test_find_public_quizzes_success(repository, mock_collection):
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value.skip.return_value.limit.return_value = [
        {"quizId": "1", "title": "Quiz 1"}
    ]

    mock_collection.find.return_value = mock_cursor

    result = repository.find_public_quizzes(page=1, limit=10)

    assert result == [{"quizId": "1", "title": "Quiz 1"}]
    mock_collection.find.assert_called_once_with(
        {"is_public": True},
        {"quizId": 1, "title": 1, "_id": 0},
    )

def test_find_public_quizzes_error(repository, mock_collection):
    mock_collection.find.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.find_public_quizzes(page=1, limit=10)

def test_count_public_quizzes_success(repository, mock_collection):
    mock_collection.count_documents.return_value = 5

    result = repository.count_public_quizzes()

    assert result == 5
    mock_collection.count_documents.assert_called_once_with(
        {"is_public": True}
    )

def test_count_public_quizzes_error(repository, mock_collection):
    mock_collection.count_documents.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.count_public_quizzes()

def test_find_by_owner_success(repository, mock_collection):
    mock_collection.find.return_value = [
        {"quizId": "1", "ownerId": "user1"}
    ]

    result = repository.find_by_owner("user1")

    assert result == [{"quizId": "1", "ownerId": "user1"}]
    mock_collection.find.assert_called_once_with({"ownerId": "user1"})

def test_find_by_owner_error(repository, mock_collection):
    mock_collection.find.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.find_by_owner("user1")

def test_find_by_id_success(repository, mock_collection):
    mock_collection.find_one.return_value = {"quizId": "123"}

    result = repository.find_by_id("123")

    assert result == {"quizId": "123"}
    mock_collection.find_one.assert_called_once_with({"quizId": "123"})

def test_find_by_id_error(repository, mock_collection):
    mock_collection.find_one.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.find_by_id("123")

def test_insert_success(repository, mock_collection):
    quiz = {"quizId": "1"}

    repository.insert(quiz)

    mock_collection.insert_one.assert_called_once_with(quiz)

def test_insert_error(repository, mock_collection):
    mock_collection.insert_one.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.insert({"quizId": "1"})

def test_delete_success(repository, mock_collection):
    repository.delete("1")

    mock_collection.delete_one.assert_called_once_with({"quizId": "1"})

def test_delete_error(repository, mock_collection):
    mock_collection.delete_one.side_effect = PyMongoError("DB error")

    with pytest.raises(DatabaseError):
        repository.delete("1")