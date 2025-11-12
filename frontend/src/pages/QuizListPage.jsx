import "../styles/QuizListPage.css";
import {useNavigate} from "react-router-dom";
import { Trash2 } from "lucide-react";
import {useState, useEffect} from "react";
import {apiFetch} from "../api/api";
import { useAuthenticator } from "@aws-amplify/ui-react";

const CACHE_KEY = "quizListCache";
const CACHE_TTL = 10 * 1000;

async function fetchQuizzesWithCache() {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
        const {data, timestamp} = JSON.parse(cached);
        if (Date.now() - timestamp < CACHE_TTL) {
            return data;
        }
    }

    const json = await apiFetch("/quizzes");
    const quizzes = (json.quizzes || []).map(({quizId, title}) => ({id: quizId, title}));

    localStorage.setItem(
        CACHE_KEY,
        JSON.stringify({data: quizzes, timestamp: Date.now()})
    );

    return quizzes;
}

export default function QuizListPage() {
  const navigate = useNavigate();
  const { signOut } = useAuthenticator();

  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadQuizzes() {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchQuizzesWithCache();
            setQuizzes(data);
        } catch (err) {
            setError(err.message || "Unknow error");
        } finally {
            setLoading(false);
        }
    }
    loadQuizzes();
  }, []);

  const handleLogout = async () => {
    await signOut();
    navigate("/");
  };

  const handleQuizClick = (id) => navigate(`/quiz/${id}`);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    setError(null);
    try {
      await apiFetch(`/quizzes/${id}`, {method: "DELETE"});
      const updated = quizzes.filter((quiz) => quiz.id !== id);
      setQuizzes(updated);
      localStorage.setItem(
        CACHE_KEY,
        JSON.stringify({
          data: updated,
          timestamp: Date.now()
        })
      );
    } catch (error) {
      setError("Failed to delete quiz");
    }
  };

  if (loading) return <p>Loading quizzes...</p>
  if (error) return <p>Error loading quizzes: {error}</p>

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