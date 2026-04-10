import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../api/api";
import { AuthContext } from "../auth/AuthProvider";

interface Quiz {
    quizId: string;
    title: string;
}

interface QuizzesResponse {
    quizzes: Quiz[]
}

export function useMyQuizzes() {
    const navigate = useNavigate();
    const { keycloak, authenticated } = useContext(AuthContext);

    const [myQuizzes, setMyQuizzes] = useState<Quiz[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!authenticated) {
            navigate("/");
            return;
        }

        const loadMyQuizzes = async () => {
            setLoading(true);
            setError(null);

            try {
                const data: QuizzesResponse = await apiFetch(
                    "http://quiz-service:8080/quizzes/mine",
                    {},
                    true
                );

                setMyQuizzes(data.quizzes || []);
            } catch (err: any) {
                setError(err.message || "Error loading your quizzes");
            } finally {
                setLoading(false);
            }
        };

        loadMyQuizzes();
    }, [authenticated, navigate]);

    const actions = {
        logout: () => keycloak.logout({ redirectUri: window.location.origin }),

        goHome: () => navigate("/"),

        playSolo: (quizId: string) => {
            navigate(`/solo-quiz/${quizId}`);
        },

        deleteQuiz: async (quizId: string) => {
            if (!window.confirm("Are you sure you want to delete this quiz?"))
                return;

            try {
                await apiFetch(
                    `http://quiz-service:8080/quizzes/${quizId}`,
                    { method: "DELETE" },
                    true
                );

                setMyQuizzes((prev) =>
                    prev.filter((q) => q.quizId !== quizId)
                );
            } catch (err: any) {
                alert(err.message || "Failed to delete quiz");
            }
        }
    };

    return {
        state: {
            myQuizzes,
            loading,
            error,
            username: keycloak.tokenParsed?.preferred_username
        },
        actions
    };
}