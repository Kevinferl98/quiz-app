import "../../styles/createRoom/QuizSelectionList.css";

interface Quiz {
    quizId: string;
    title: string;
}

interface Props {
    quizzes: Quiz[];
    loading: boolean;
    error: string | null;
    creatingRoomId: string | null;
    onCreateRoom: (quizId: string) => void;
}

export function QuizSelectionList({
    quizzes,
    loading,
    error,
    creatingRoomId,
    onCreateRoom
}: Props) {
    return (
        <div className="quiz-list-section">
            <h2>Select a Quiz</h2>

            {loading && <p>Loading quizzes...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && quizzes.length === 0 && (
                <p>No quizzes available.</p>
            )}

            <ul className="quiz-list">
                {quizzes.map((quiz) => (
                    <li key={quiz.quizId}>
                        <span>{quiz.title}</span>
                        <button
                            className="primary-btn"
                            onClick={() => onCreateRoom(quiz.quizId)}
                            disabled={creatingRoomId === quiz.quizId}
                        >
                            {creatingRoomId === quiz.quizId ? "Creating..." : "Create Room"}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}