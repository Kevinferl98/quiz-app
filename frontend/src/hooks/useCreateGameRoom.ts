import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/api";
import { AuthContext } from "../auth/AuthProvider";

interface Quiz {
    quizId: string;
    title: string;
}

interface QuizzesResponse {
    quizzes: Quiz[];
}

export function useCreateGameRoom() {
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
        const loadQuizzes = async () => {
            setLoading(true);
            setError(null);

            try {
                const data: QuizzesResponse = await apiFetch(
                    "/quizzes/public"
                );
                setQuizzes(data.quizzes || []);
            } catch(err: any) {
                setError(err.message || "Error loading quizzes");
            } finally {
                setLoading(false);
            }
        };

        if (authenticated) {
            loadQuizzes();
        }
    }, [authenticated]);

    const actions = {
        goHome: () => navigate("/"),

        logout: () => keycloak.logout({ redirectUri: window.location.origin }),

        creteRoom: async (quizId: string) => {
            try {
                setCreatingRoomId(quizId);

                const room = await apiFetch(
                    `/game/${quizId}/create_room`,
                    { method: "POST" },
                    true
                );

                navigate(`/room/${room.room_id}`);
            } catch (err: any) {
                alert(err.message || "Error creating room");
            } finally {
                setCreatingRoomId(null);
            }
        }
    };

    return {
        state: {
            quizzes,
            loading,
            error,
            creatingRoomId,
            authenticated
        },
        actions
    };
}