from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@patch("app.services.quiz_service.quiz_table.scan")
def test_list_public_quizzes(mock_scan):
    mock_scan.return_value = {"Items": [{"quizId": "1", "title": "Quiz 1"}]}
    response = client.get("/quizzes/public")
    assert response.status_code == 200
    assert response.json() == {"quizzes": [{"quizId": "1", "title": "Quiz 1"}]}

@patch("app.services.quiz_service.quiz_table.scan")
def test_list_public_quizzes_db_error(mock_scan):
    mock_scan.side_effect = Exception("DynamoDB connection failed")
    
    response = client.get("/quizzes/public")
    
    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred while accessing the database"}

@patch("app.services.quiz_service.quiz_table.scan")
def test_list_my_quizzes(mock_scan):
    mock_scan.return_value = {"Items": [{"quizId": "2", "title": "My Quiz"}]}
    response = client.get("/quizzes/mine")
    assert response.status_code == 200
    assert response.json() == {"quizzes": [{"quizId": "2", "title": "My Quiz"}]}

@patch("app.services.quiz_service.quiz_table.get_item")
def test_get_quiz_success(mock_get_item):
    mock_get_item.return_value = {
        "Item": {"quizId": "abc-123", "title": "Test Quiz", "owner_id": "user_123"}
    }
    response = client.get("/quizzes/abc-123")
    assert response.status_code == 200
    assert response.json()["quizId"] == "abc-123"

@patch("app.services.quiz_service.quiz_table.get_item")
def test_get_quiz_not_found(mock_get_item):
    mock_get_item.return_value = {}
    
    response = client.get("/quizzes/non-existent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Quiz not found"

@patch("app.services.quiz_service.quiz_table.put_item")
def test_create_quiz(mock_put_item):
    quiz_data = {
        "title": "New Quiz",
        "questions": [{"id": "q1", "question_text": "Text", "options": ["A", "B"], "correct_option": "A"}]
    }
    response = client.post("/quizzes/", json=quiz_data)
    assert response.status_code == 200
    called_item = mock_put_item.call_args[1]["Item"]
    assert called_item["owner_id"] == "user_123"

@patch("app.services.quiz_service.quiz_table.delete_item")
@patch("app.services.quiz_service.quiz_table.get_item")
def test_delete_quiz_success(mock_get_item, mock_delete_item):
    mock_get_item.return_value = {
        "Item": {"quizId": "abc-123", "owner_id": "user_123"}
    }
    response = client.delete("/quizzes/abc-123")
    assert response.status_code == 200
    mock_delete_item.assert_called_once()

@patch("app.services.quiz_service.quiz_table.get_item")
def test_delete_quiz_forbidden(mock_get_item):
    mock_get_item.return_value = {
        "Item": {"quizId": "abc-123", "owner_id": "someone_else"}
    }
    response = client.delete("/quizzes/abc-123")
    assert response.status_code == 403

@patch("app.services.quiz_service.quiz_table.get_item")
def test_answer_question(mock_get_quiz):
    mock_get_quiz.return_value = {
        "Item": {
            "quizId": "abc-123",
            "title": "New Quiz",
            "questions": [
                {"id": "q1", "question_text": "Text", "options": ["A", "B"], "correct_option": "A"}
            ]
        }
    }

    payload = {
        "question_id": "q1",
        "answer": "A"
    }

    response = client.post("/quizzes/abc-123/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["correct"] is True