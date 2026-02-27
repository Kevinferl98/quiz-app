import { useEffect, useRef, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../auth/AuthProvider";
import "../styles/RoomPage.css";

interface LeaderboardEntry {
    name: string;
    score: number;
}

export default function RoomPage() {
    const { room_id } = useParams();
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);
    
    const wsRef = useRef<WebSocket | null>(null);
    const playerIdRef = useRef<string>("");

    const [role, setRole] = useState<"host" | "player">("player");
    const [players, setPlayers] = useState<string[]>([]);
    const [question, setQuestion] = useState<any>(null);
    const [timer, setTimer] = useState<number>(0);
    const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
    const [gameEnded, setGameEnded] = useState(false);

    const [connected, setConnected] = useState(false);
    const [nameInput, setNameInput] = useState("");
    const [nameSubmitted, setNameSubmitted] = useState(false);

    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [correctAnswer, setCorrectAnswer] = useState<string | null>(null);

    const connectWebSocket = (playerId: string, username?: string) => {
        if (!room_id) return;

        const tokenQuery = authenticated && keycloak.token ? `?token=${keycloak.token}` : "";
        const ws = new WebSocket(`ws://game-service:8002/ws/rooms/${room_id}${tokenQuery}`);
        wsRef.current = ws;

        ws.onopen = () => {
            setConnected(true);
            if (username && role !== "host") {
                ws.send(JSON.stringify({type: "join", name: username}));
            }
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);

            switch (data.type) {
                case "role":
                    setRole(data.role);
                    playerIdRef.current = data.player_id;
                    if (authenticated && data.role !== "host") {
                        ws.send(JSON.stringify({ type: "join", name: keycloak.tokenParsed?.preferred_username }));
                    }
                    break;
                case "player_joined":
                case "player_left":
                    setPlayers(data.players);
                    break;
                case "question":
                    setQuestion(data.question);
                    setLeaderboard([]);
                    setSelectedAnswer(null);
                    setCorrectAnswer(null);
                    break;
                case "timer":
                    setTimer(data.seconds);
                    break;
                case "answer_result":
                    setCorrectAnswer(data.correct_answer);
                    break;
                case "leaderboard":
                    setLeaderboard(data.leaderboard);
                    break;
                case "end":
                    setLeaderboard(data.leaderboard);
                    setGameEnded(true);
                    break;
                case "error":
                    alert(data.message);
                    break;
            }
        };

        ws.onclose = () => setConnected(false);
    };

    useEffect(() => {
        if (!room_id) return;

        if (authenticated) {
            const playerId = keycloak.tokenParsed?.sub as string;
            const username = keycloak.tokenParsed?.preferred_username as string;
            playerIdRef.current = playerId;
            connectWebSocket(playerId, username);
            setNameSubmitted(true);
        }
    }, [authenticated, room_id]);

    const handleSubmitName = () => {
        if (!nameInput.trim()) return;
        const uuid = crypto.randomUUID();
        playerIdRef.current = uuid;
        connectWebSocket(uuid, nameInput.trim());
        setNameSubmitted(true);
    }

    const handleStart = () => {
        wsRef.current?.send(JSON.stringify({ type: "start"}));
    };

    const handleAnswer = (answer: string) => {
        if (selectedAnswer) return;
        setSelectedAnswer(answer);
        wsRef.current?.send(JSON.stringify({ type: "answer", answer }));
    };

    if (!authenticated && !nameSubmitted) {
        return (
            <div className="room-container">
                <h2>Enter your name to join</h2>
                <input
                    type="text"
                    placeholder="Your name"
                    value={nameInput}
                    onChange={(e) => setNameInput(e.target.value)} 
                ></input>
                <button className="primary-btn" onClick={handleSubmitName}>Join Room</button>
            </div>
        );
    }

    return (
        <div className="room-container">
            <div className="top-bar">
                <button className="primary-btn" onClick={() => navigate("/")}>Back to Home</button>
                <span className="room-id">Room ID: {room_id}</span>
            </div>

            {!question && !gameEnded && (
                <>
                    <h2>Waiting Room</h2>
                    <p>Players:</p>
                    <ul>
                        {players.map((p, i) => (
                            <li key={i}>{p}</li>
                        ))}
                    </ul>

                    {role === "host" && (
                        <button className="primary-btn start-btn" onClick={handleStart}>
                            Start Quiz
                        </button>
                    )}
                </>
            )}
            
            {question && (
                <div className="question-box">
                    <h2>{question.question_text}</h2>
                    <p>Time left: {timer}s</p>
                    <div className="options">
                        {question.options.map((opt: string, i: number) => {
                            let className = "option-btn";

                            if (selectedAnswer === opt) {
                                className += " selected";
                            }

                            if (correctAnswer) {
                                if (opt === correctAnswer) {
                                    className += " correct";
                                } else if (opt === selectedAnswer) {
                                    className += " wrong";
                                }
                            }

                            return (
                                <button
                                    key={i}
                                    className={className}
                                    onClick={() => handleAnswer(opt)}
                                    disabled={!!selectedAnswer}
                                >{opt}
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}

            {leaderboard.length > 0 && (
                <div className="leaderboard">
                    <h2>Leaderboard</h2>
                    {leaderboard.map((entry, i) => (
                        <div key={i}>
                            {entry.name} - {entry.score}
                        </div>
                    ))}
                </div>
            )}

            {gameEnded && <h2>Game Finished!</h2>}
        </div>
    )
}