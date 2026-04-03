import pytest
from unittest.mock import MagicMock, patch
from app.exception import QuizNotFoundError, QuizPermissionError, QuestionNotFoundError
from app.services.quiz_service import QuizService
from app.schemas.quiz import QuizCreateRequest, Question

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return QuizService(repo=mock_repo)

def test_list_public_quizzes(service, mock_repo):
    mock_repo.find_public_quizzes.return_value = [{"quizId": "1", "title": "Public Quiz"}]
    result = service.list_public_quizzes()
    assert len(result) == 1
    assert result[0]["title"] == "Public Quiz"
    mock_repo.find_public_quizzes.assert_called_once()

def test_list_personal_quizzes(service, mock_repo):
    mock_repo.find_by_owner.return_value = [{"quizId": "1", "title": "Personal Quiz"}]
    result = service.list_personal_quizzes("user_1")
    assert len(result) == 1
    mock_repo.find_by_owner.assert_called_once_with("user_1")

def test_create_quiz_generates_uuid(service, mock_repo):
    quiz_data = QuizCreateRequest(
        title="New Quiz",
        questions=[Question(id="q1", question_text="Question 1", options=["Option 1", "Option 2"], correct_option="A")],
    )

    fixed_uuid = "12345678-1234-5678-1234-567812345678"
    with patch("uuid.uuid4", return_value=fixed_uuid):
        quiz_id = service.create_quiz(quiz_data, owner_id="user_123")

    assert quiz_id == fixed_uuid
    args, _ = mock_repo.insert.call_args
    inserted_data = args[0]
    assert inserted_data["quizId"] == fixed_uuid
    assert inserted_data["owner_id"] == "user_123"
    assert inserted_data["title"] == "New Quiz"

def test_delete_quiz_success(service, mock_repo):
    mock_repo.find_by_id.return_value = {"quizId": "q_1", "owner_id": "user_1"}

    service.delete_quiz("q_1", "user_1")

    mock_repo.delete.assert_called_once_with("q_1")

def test_delete_quiz_not_found(service, mock_repo):
    mock_repo.find_by_id.return_value = None

    with pytest.raises(QuizNotFoundError):
        service.delete_quiz("invalid", "user_1")

def test_delete_quiz_permission_error(service, mock_repo):
    mock_repo.find_by_id.return_value = {"quizId": "q_1", "owner_id": "owner_real"}

    with pytest.raises(QuizPermissionError):
        service.delete_quiz("q_1", "hacker_user")

def test_check_answer_correct(service, mock_repo):
    mock_repo.find_by_id.return_value = {
        "questions": [
            {"id": "q1", "correct_option": "A"},
            {"id": "q2", "correct_option": "B"}
        ]
    }

    assert service.check_answer("quiz_1", "q1", "A") is True
    assert service.check_answer("quiz_1", "q1", "B") is False

def test_check_answer_question_not_found(service, mock_repo):
    mock_repo.find_by_id.return_value = {"questions": [{"id": "q1"}]}

    with pytest.raises(QuestionNotFoundError):
        service.check_answer("quiz_1", "non_existent_q", "A")

def test_check_answer_quiz_not_found(service, mock_repo):
    mock_repo.find_by_id.return_value = None

    with pytest.raises(QuizNotFoundError):
        service.check_answer("missing_quiz", "q1", "A")