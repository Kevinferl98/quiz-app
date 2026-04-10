import "../../styles/home/MainActions.css";

export function MainActions({
    authenticated,
    onCreateQuiz,
    onCreateRoom,
    onMyQuizzes
}: any) {
    return (
        <div className="main-actions">
            <button className="primary-btn success-btn" onClick={onCreateQuiz}>Create New Quiz</button>
            <button className="primary-btn success-btn" onClick={onCreateRoom}>Create New Room</button>

            {authenticated && (
                <button className="primary-btn success-btn" onClick={onMyQuizzes}>My Quizzes</button>
            )}
        </div>
    );
}