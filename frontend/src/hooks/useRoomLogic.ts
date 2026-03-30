import { useEffect, useRef, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../auth/AuthProvider";

export function useRoomLogic() {
    const { room_id } = useParams();
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);
    
    const wsRef = useRef<WebSocket | null>(null);
    const playerIdRef = useRef<string>("");

    const [role, setRole] = useState<"host" | "player">("player");
    const [players, setPlayers] = useState<string[]>([]);
    const [question, setQuestion] = useState<any>(null);
    const [timer, setTimer] = useState<number>(0);
    const [leaderboard, setLeaderboard] = useState<any[]>([]);
    const [gameEnded, setGameEnded] = useState(false);

    const [connected, setConnected] = useState(false);
    const [nameInput, setNameInput] = useState("");
    const [nameSubmitted, setNameSubmitted] = useState(false);

    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [correctAnswer, setCorrectAnswer] = useState<string | null>(null);

    const [isFinalLeaderboard, setIsFinalLeaderboard] = useState(false);
    const [totalTime, setTotalTime] = useState<number>(15);
    const [redirect, setRedirect] = useState<string | null>(null);

    const connectWebSocket = (playerId: string, username?: string) => {
        if (!room_id) return;
        const tokenQuery = authenticated && keycloak.token ? `?token=${keycloak.token}` : "";
        const ws = new WebSocket(`ws://nginx-lb:8082/ws/rooms/${room_id}${tokenQuery}`);
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
                    const duration = data.question.duration || 15;
                    setTimer(duration);
                    setTotalTime(duration);
                    break;
                case "timer":
                    setTimer(data.seconds);
                    break;
                case "answer_result":
                    setCorrectAnswer(data.correct_answer);
                    break;
                case "leaderboard":
                    setQuestion(null);
                    setLeaderboard(data.leaderboard);
                    setIsFinalLeaderboard(!!data.final);
                    break;
                case "error":
                    if (data.code === "ROOM_NOT_FOUND" || data.code === "ROOM_ALREADY_STARTED") {
                        alert(data.message);
                        setRedirect("/");
                    } else {
                        alert(data.message);
                    }
                    break;
            }
        };
        ws.onclose = () => setConnected(false);
    };

    useEffect(() => {
        if (timer <= 0) return;
        const interval = setInterval(() => {
            setTimer((t) => {
                if (t <= 1) {
                    clearInterval(interval);
                    return 0;
                }
                return t - 1;
            });
        }, 1000);
        return () => clearInterval(interval);
    }, [timer]);

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

    useEffect(() => {
        if (isFinalLeaderboard) setGameEnded(true);
    }, [isFinalLeaderboard]);

    useEffect(() => {
        if (redirect) navigate(redirect);
    }, [redirect, navigate]);

    const handleSubmitName = () => {
        if (!nameInput.trim()) return;
        const uuid = crypto.randomUUID();
        playerIdRef.current = uuid;
        connectWebSocket(uuid, nameInput.trim());
        setNameSubmitted(true);
    };

    const handleStart = () => wsRef.current?.send(JSON.stringify({ type: "start"}));
    
    const handleAnswer = (answer: string) => {
        if (selectedAnswer) return;
        setSelectedAnswer(answer);
        wsRef.current?.send(JSON.stringify({ type: "answer", answer }));
    };

    const disconnectAndGoHome = () => {
        wsRef.current?.close();
        navigate("/");
    };

    return {
        state: { room_id, role, players, question, timer, leaderboard, gameEnded, nameInput, nameSubmitted, selectedAnswer, correctAnswer, isFinalLeaderboard, totalTime, authenticated },
        actions: { setNameInput, handleSubmitName, handleStart, handleAnswer, disconnectAndGoHome }
    };
}