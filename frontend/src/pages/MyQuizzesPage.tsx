import { useState, useEffect, useContext, use } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/api";
import { AuthContext } from "../auth/AuthProvider";
import "../styles/MyQuizzesPage.css";

interface Quiz {
    quizId: string;
    title: string;
}

interface QuizzesResponse {
    quizzes: Quiz[]
}

export default function MyQuizzesPage() {
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);

    const [myQuizzes, setMyQuizzes] = useState<Quiz[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const handleLogout = () => keycloak.logout({ redirectUri: window.location.origin });

    const handleSoloQuiz = (quizId: string) => {
        navigate(`/solo-quiz/${quizId}`);
    };

    const handleDeleteQuiz = async (quizId: string) => {
        if (!window.confirm("Are you sure you want to delete this quiz?")) return;

        try {
            await apiFetch(`http://quiz-service:8080/quizzes/${quizId}`, {
                method: "DELETE"
            }, true);
            setMyQuizzes(prev => prev.filter(q => q.quizId !== quizId));
        } catch (err: any) {
            alert(err.message || "Failed to delete quiz");
        }
    };

    const handleBackToHome = () => {
        navigate("/");
    };

    useEffect(() => {
        if (!authenticated) {
            navigate("/");
            return;
        }

        async function loadMyQuizzes() {
            setLoading(true);
            setError(null);
            try {
                const data: QuizzesResponse = await apiFetch("http://quiz-service:8080/quizzes/mine", {}, true);
                setMyQuizzes(data.quizzes || []);
            } catch (err: any) {
                setError(err.message || "Error loading your quizzes");
            } finally {
                setLoading(false);
            }
        }

        loadMyQuizzes();
    }, [authenticated, navigate]);

    return (
        <div className="home-container">
            <div className="top-bar">
                <button className="back-btn" onClick={handleBackToHome}>← Back to Home</button>
                <div className="auth-section">
                    <span>Welcome {keycloak.tokenParsed?.preferred_username}</span>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            </div>

            <h1>My Quizzes</h1>

            {loading && <p>Loading your quizzes....</p>}
            {error && <p className="error">{error}</p>}
            {!loading && myQuizzes.length === 0 && <p>You haven't created any quizzes yet.</p>}

            <ul className="quiz-list">
                {myQuizzes.map((quiz) => (
                    <li key={quiz.quizId}>
                        <span>{quiz.title}</span>
                        <button onClick={() => handleSoloQuiz(quiz.quizId)}>Play solo</button>
                        <button onClick={() => handleDeleteQuiz(quiz.quizId)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}