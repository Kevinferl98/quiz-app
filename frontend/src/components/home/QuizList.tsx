import "../../styles/home/QuizList.css";

export function QuizList({ quizzes, loading, error, onPlay }: any) {
    return (
        <div className="mq-list-wrapper">
            <h2 className="mq-section-title">Explore Quizzes</h2>

            {loading && <div className="mq-loader">Loading...</div>}
            {error && <div className="mq-error-msg">{error}</div>}
            
            {!loading && !error && quizzes.length === 0 && (
                <div className="mq-empty-state">No quizzes available at the moment.</div>
            )}

            <div className="mq-grid-quizzes">
                {quizzes.map((quiz: any) => (
                    <div key={quiz.quizId} className="mq-quiz-card">
                        <div className="mq-quiz-info">
                            <h3>{quiz.title}</h3>
                            <p></p>
                        </div>
                        <button className="mq-btn-play" onClick={() => onPlay(quiz.quizId)}>
                            Play
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}