export function QuizList({ quizzes, loading, error, onPlay }: any) {
    return (
        <div className="quiz-list-section">
            <h2>Available Quizzes</h2>

            {loading && <p>Loading quizzes...</p>}
            {error && <p className="error">{error}</p>}
            {!loading && !error && quizzes.length === 0 && (
                <p>No quizzes available.</p>
            )}

            <ul className="quiz-list">
                {quizzes.map((quiz: any) => (
                    <li key={quiz.quizId}>
                        <span>{quiz.title}</span>
                        <button onClick={() => onPlay(quiz.quizId)}>
                            Play solos
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}