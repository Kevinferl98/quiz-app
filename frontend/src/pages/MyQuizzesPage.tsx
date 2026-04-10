import { useMyQuizzes } from "../hooks/useMyQuizzes";
import { TopBar } from "../components/myQuizzes/TopBar";
import { MyQuizList } from "../components/myQuizzes/MyQuizList";
import "../styles/myQuizzes/MyQuizzesPage.css"

export default function MyQuizzesPage() {
    const { state, actions } = useMyQuizzes();

    return (
        <div className="home-container">
            <TopBar
                username={state.username}
                onBack={actions.goHome}
                onLogout={actions.logout}
            />

            <h1>My Quizzes</h1>

            <MyQuizList
                quizzes={state.myQuizzes}
                loading={state.loading}
                error={state.error}
                onPlay={actions.playSolo}
                onDelete={actions.deleteQuiz}
            />
        </div>
    );
}