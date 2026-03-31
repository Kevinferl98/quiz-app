import { useEffect, useRef, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { AuthContext } from "../auth/AuthProvider";

type Role = "host" | "player";

type Question = {
    text: string;
    options: string[];
    duration?: number;
};

type LeaderboardEntry = {
    name: string;
    score: number;
}

type RoomViewState = 
    | "ENTER_NAME"
    | "WAITING"
    | "QUESTION"
    | "LEADERBOARD"
    | "FINISHED";

export function useRoomLogic() {
    const { room_id } = useParams();
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);
    
    const wsRef = useRef<WebSocket | null>(null);
    const playerIdRef = useRef<string>("");

    const [role, setRole] = useState<Role>("player");
    const [players, setPlayers] = useState<string[]>([]);
    const [question, setQuestion] = useState<Question | null>(null);
    const [timer, setTimer] = useState<number>(0);
    const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);

    const [connected, setConnected] = useState(false);

    const [nameInput, setNameInput] = useState("");
    const [nameSubmitted, setNameSubmitted] = useState(false);

    const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
    const [correctAnswer, setCorrectAnswer] = useState<string | null>(null);

    const [isFinalLeaderboard, setIsFinalLeaderboard] = useState(false);
    const [totalTime, setTotalTime] = useState<number>(15);

    const [redirect, setRedirect] = useState<string | null>(null);

    const getViewState = (): RoomViewState => {
        if (!authenticated && !nameSubmitted) return "ENTER_NAME";
        
        if (question) return "QUESTION";
        
        if (leaderboard.length > 0) {
            return isFinalLeaderboard ? "FINISHED" : "LEADERBOARD";
        }

        return "WAITING";
    };

    const send = (payload: object) => {
        wsRef.current?.send(JSON.stringify(payload));
    };

    const disconnect = () => {
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
    };

    const handleNewQuestion = (q: Question) => {
        setQuestion(q);
        setLeaderboard([]);
        setSelectedAnswer(null);
        setCorrectAnswer(null);

        const duration = q.duration || 15;
        setTimer(duration);
        setTotalTime(duration);
    };

    const handleLeaderboard = (data: any) => {
        setQuestion(null);
        setLeaderboard(data.leaderboard);
        setIsFinalLeaderboard(!!data.final);
    };

    const handleError = (data: any) => {
        alert(data.message);

        if (
            data.code === "ROOM_NOT_FOUND" ||
            data.code === "ROOM_ALREADY_STARTED"
        ) {
            setRedirect("/");
        }
    };

    const handleMessage = (ws: WebSocket, data: any) => {
        switch (data.type) {
            case "role":
                setRole(data.role);
                playerIdRef.current = data.player_id;

                if (authenticated && data.role !== "host") {
                    send({
                        type: "join",
                        name: keycloak.tokenParsed?.preferred_username
                    });
                }
                break;

            case "player_joined":
            case "player_left":
                setPlayers(data.players);
                break;

            case "question":
                handleNewQuestion(data.question);
                break;

            case "timer":
                setTimer(data.seconds);
                break;

            case "answer_result":
                setCorrectAnswer(data.correct_answer);
                break;

            case "leaderboard":
                handleLeaderboard(data);
                break;

            case "error":
                handleError(data);
                break;
        }
    };

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
            handleMessage(ws, data);
        };

        ws.onclose = () => {
            setConnected(false);
        };
    };

    // Timer countdown
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

    // Auth auto join
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

    // Redirect
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

    const handleStart = () => {
        send({ type: "start" })
    };
    
    const handleAnswer = (answer: string) => {
        if (selectedAnswer) return;

        setSelectedAnswer(answer);
        send({ type: "answer", answer })
    };

    const disconnectAndGoHome = () => {
        disconnect();
        navigate("/");
    };

    return {
        state: {
            room_id,
            role,
            players,
            question,
            timer,
            leaderboard,
            nameInput,
            nameSubmitted,
            selectedAnswer,
            correctAnswer,
            isFinalLeaderboard,
            totalTime,
            authenticated,
            viewState: getViewState()
        },
        actions: {
            setNameInput,
            handleSubmitName,
            handleStart,
            handleAnswer,
            disconnectAndGoHome
        }
    };
}