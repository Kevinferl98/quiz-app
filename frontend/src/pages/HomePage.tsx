import { useState, useEffect, ChangeEvent, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/api";
import { AuthContext } from "../auth/AuthProvider";
import "../styles/HomePage.css";

interface Quiz {
  quizId: string;
  title: string;
}

interface QuizzesReponse {
  quizzes: Quiz[]
}

export default function HomePage() {
  const navigate = useNavigate();

  // Quiz list and room code
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [roomCode, setRoomCode] = useState<string>("");
  
  const { keycloak, authenticated } = useContext(AuthContext);
  const handleLogin = () => keycloak.login();
  const handleLogout = () => keycloak.logout({ redirectUri: window.location.origin });

  // Load quizzes
  useEffect(() => {
    async function loadQuizzes() {
      setLoading(true);
      setError(null);
      try {
        const data: QuizzesReponse = await apiFetch("http://quiz-service:8080/quizzes/public");
        setQuizzes(data.quizzes || []);
      } catch (err: any) {
        setError(err.message || "Error loading quizzes");
      } finally {
        setLoading(false);
      }
    }
    loadQuizzes();
  }, []);

  const handleJoinRoom = () => {
    if (!roomCode.trim()) {
      alert("Please enter a valid room code.");
      return;
    }
    navigate(`/room/${roomCode}`);
  };

  const handleSoloQuiz = (quizId: string) => {
    navigate(`/solo-quiz/${quizId}`);
  };

  const handleCreateQuiz = () => {
    if (!authenticated) {
      keycloak.login();
      return;
    }
    navigate("/create");
  }
  const handleCreateRoom = () => {
    if (!authenticated) {
      keycloak.login();
      return;
    }
    navigate("/create-room"); 
  }
  const handleRoomCodeChange = (e: ChangeEvent<HTMLInputElement>) => {
    setRoomCode(e.target.value);
  };

  return (
    <div className="home-container">
      <div className="auth-bar">
        {!authenticated ? (
          <button onClick={handleLogin}>Login / Sign Up</button>
        ) : (
          <>
            <span>
              Welcome {keycloak.tokenParsed?.preferred_username}
            </span>
            <button onClick={handleLogout}>Logout</button>
          </>
        )}
      </div>
      <h1>Quiz App</h1>

      {/* Room code input */}
      <div className="join-room">
        <input
          type="text"
          placeholder="Enter room code"
          value={roomCode}
          onChange={(e) => setRoomCode(e.target.value)}
        />
        <button onClick={handleJoinRoom}>Join Room</button>
      </div>

      {/* Main action buttons */}
      <div className="main-actions">
        <button onClick={handleCreateQuiz}>Create New Quiz</button>
        <button onClick={handleCreateRoom}>Create New Room</button>
      </div>

      {/* Available quizzes list */}
      <div className="quiz-list-section">
        <h2>Available Quizzes</h2>
        {loading && <p>Loading quizzes...</p>}
        {error && <p className="error">{error}</p>}
        {!loading && !error && quizzes.length === 0 && <p>No quizzes available.</p>}
        <ul className="quiz-list">
          {quizzes.map((quiz) => (
            <li key={quiz.quizId}>
              <span>{quiz.title}</span>
              <button onClick={() => handleSoloQuiz(quiz.quizId)}>Play solo</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
