import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/api";
import { AuthContext } from "../auth/AuthProvider";
import "../styles/CreateGameRoom.css";

interface Quiz {
    quizId: string;
    title: string;
}

interface QuizzesResponse {
    quizzes: Quiz[];
}

export default function CreateGameRoom() {
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);

    const [quizzes, setQuizzes] = useState<Quiz[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [creatingRoomId, setCreatingRoomId] = useState<string | null>(null);

    useEffect(() => {
        if (!authenticated) {
            keycloak.login();
        }
    }, [authenticated, keycloak]);

    useEffect(() => {
        async function loadQuizzes() {
            setLoading(true);
            setError(null);

            try {
                const data: QuizzesResponse = await apiFetch(
                    "http://quiz-service:8001/quizzes/public"
                );
                setQuizzes(data.quizzes || []);
            } catch(err: any) {
                setError(err.message || "Error loading quizzes");
            } finally {
                setLoading(false);
            }
        }

        if (authenticated) {
            loadQuizzes();
        }
    }, [authenticated]);

    const handleCreateRoom = async (quizId: string) => {
        try {
            setCreatingRoomId(quizId);

            const room = await apiFetch(
                `http://game-service:8002/quizzes/${quizId}/create_room`,
                {
                    method: "POST"
                },
                true
            );
            console.log("room created");
            //navigate(`/room/${room.roomId}`);
        } catch (err: any) {
            alert(err.message || "Error creating room");
        } finally {
            setCreatingRoomId(null);
        }
    };

    return (
        <div className="create-room-container">
            <div className="top-bar">
                <button onClick={() => navigate("/")}>← Back to Home</button>
                <button onClick={() => keycloak.logout({ redirectUri: window.location.origin})}>Logout</button>
            </div>

            <h1>Create Game Room</h1>

            <div className="quiz-list-section">
                <h2>Select a Quiz</h2>

                {loading && <p>Loading quizzes...</p>}
                {error && <p className="error">{error}</p>}
                {!loading && quizzes.length === 0 && <p>No quizzes available.</p>}

                <ul className="quiz-list">
                    {quizzes.map((quiz) => (
                        <li key={quiz.quizId}>
                            <span>{quiz.title}</span>
                            <button onClick={() => handleCreateRoom(quiz.quizId)} disabled={creatingRoomId === quiz.quizId}>
                                {creatingRoomId === quiz.quizId ? "Creating" : "Create Room"}
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}