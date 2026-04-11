import "../../styles/home/MainActions.css";

export function MainActions({ authenticated, onCreateQuiz, onCreateRoom, onMyQuizzes }: any) {
    return (
        <div className="mq-actions-grid">
            <button className="mq-action-card create" onClick={onCreateQuiz}>
                <span className="mq-icon">➕</span>
                <span>Create Quiz</span>
            </button>
            
            <button className="mq-action-card room" onClick={onCreateRoom}>
                <span className="mq-icon">🏠</span>
                <span>Create Room</span>
            </button>

            {authenticated && (
                <button className="mq-action-card profile" onClick={onMyQuizzes}>
                    <span className="mq-icon">👤</span>
                    <span>My Quizzes</span>
                </button>
            )}
        </div>
    );
}