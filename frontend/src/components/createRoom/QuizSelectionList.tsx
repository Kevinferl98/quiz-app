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
        <div className="mq-selection-container">
            <h2 className="mq-section-title">Select a Quiz</h2>

            {loading && (
                <div className="mq-loader-container">
                    <div className="mq-loader"></div>
                    <p>Loading your quizzes...</p>
                </div>
            )}
            
            {error && <div className="mq-error-banner">{error}</div>}

            {!loading && !error && quizzes.length === 0 && (
                <div className="mq-empty-card">
                    <p>You haven't created any quizzes yet.</p>
                </div>
            )}

            <div className="mq-quiz-selection-grid">
                {quizzes.map((quiz) => (
                    <div key={quiz.quizId} className="mq-selection-card">
                        <div className="mq-selection-info">
                            <h3>{quiz.title}</h3>
                            <span className="mq-badge">Ready Quiz</span>
                        </div>
                        
                        <button
                            className="mq-btn-launch"
                            onClick={() => onCreateRoom(quiz.quizId)}
                            disabled={creatingRoomId === quiz.quizId}
                        >
                            {creatingRoomId === quiz.quizId ? (
                                <>
                                    <span className="mq-spinner-sm"></span>
                                    Opening...
                                </>
                            ) : (
                                "Open Room"
                            )}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}