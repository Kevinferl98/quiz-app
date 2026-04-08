export function MainActions({
    authenticated,
    onCreateQuiz,
    onCreateRoom,
    onMyQuizzes
}: any) {
    return (
        <div className="main-actions">
            <button onClick={onCreateQuiz}>Create New Quiz</button>
            <button onClick={onCreateRoom}>Create New Room</button>

            {authenticated && (
                <button onClick={onMyQuizzes}>My Quizzes</button>
            )}
        </div>
    );
}