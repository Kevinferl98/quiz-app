import "../../styles/myQuizzes/MyQuizList.css"

interface Quiz {
    quizId: string;
    title: string;
}

interface Props {
    quizzes: Quiz[];
    loading: boolean;
    error: string | null;
    onPlay: (quizId: string) => void;
    onDelete: (quizId: string) => void;
}

export function MyQuizList({
    quizzes,
    loading,
    error,
    onPlay,
    onDelete
}: Props) {
    return (
        <>
            {loading && <p>Loading your quizzes...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && quizzes.length === 0 && (
                <p>You haven't created any quizzes yet.</p>
            )}

            <ul className="quiz-list">
                {quizzes.map((quiz) => (
                    <li key={quiz.quizId}>
                        <span>{quiz.title}</span>

                        <div className="actions">
                            <button
                                className="primary-btn"
                                onClick={() => onPlay(quiz.quizId)}
                            >
                                Paly solo
                            </button>

                            <button
                                className="primary-btn danger-btn"
                                onClick={() => onDelete(quiz.quizId)}
                            >
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
        </>
    );
}