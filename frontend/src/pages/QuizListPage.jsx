import "../styles/QuizListPage.css";
import {useNavigate} from "react-router-dom";
import { Trash2 } from "lucide-react";

export default function QuizListPage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // TODO
    navigate("/");
  };

  const handleGoToResults = () => {
    navigate("/results");
  }

  const quizzes = [
    { id: 1, title: "Lorem Ipsum" },
    { id: 2, title: "Lorem Ipsum" },
    { id: 3, title: "Lorem Ipsum" },
  ];

  const handleQuizClick = (id) => {
    navigate(`/quiz/${id}`);
  };

  const handleDelete = (id, e) => {
    // TODO
    e.stopPropagation();
    console.log("Deleted quiz: {}", id)
  }

  return (
    <div>
      <div className="topbar">
        <h1 className="topbar-title">Quiz App</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>

      <div className="page-content">
        <h2 className="page-title">Available Quizzes</h2>
        <div className="page-header">
          <button onClick={() => navigate("/create")} className="create-quiz-button">Create Quiz</button>
          <button onClick={() => navigate("/results")} className="results-button">Results</button>
        </div>

        <ul className="quiz-list">
          {quizzes.map((quiz) => (
            <li 
              key={quiz.id} 
              className="quiz-item"
              onClick={() => handleQuizClick(quiz.id)}>
              <span>{quiz.title}</span>
              <button className="delete-button" onClick={(e) => handleDelete(quiz.id, e)} title="Delete quiz">
                <Trash2 size={18} color="#dc2626"></Trash2>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}