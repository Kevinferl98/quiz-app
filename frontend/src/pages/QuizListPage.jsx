import "./QuizListPage.css";
import {useNavigate} from "react-router-dom";

export default function QuizListPage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  const quizzes = [
    { id: 1, title: "Lorem Ipsum" },
    { id: 2, title: "Lorem Ipsum" },
    { id: 3, title: "Lorem Ipsum" },
  ];

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
        <ul className="quiz-list">
          {quizzes.map((quiz) => (
            <li key={quiz.id} className="quiz-item">
              {quiz.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}