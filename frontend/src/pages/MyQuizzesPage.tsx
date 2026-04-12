import { useMyQuizzes } from "../hooks/useMyQuizzes";
import { TopBar } from "../components/myQuizzes/TopBar";
import { MyQuizList } from "../components/myQuizzes/MyQuizList";
import "../styles/myQuizzes/MyQuizzesPage.css"

export default function MyQuizzesPage() {
    const { state, actions } = useMyQuizzes();

    return (
        <div className="mq-container">
            <header className="mq-header">
                <TopBar
                    username={state.username}
                    onBack={actions.goHome}
                    onLogout={actions.logout}
                />
            </header>

            <main className="mq-main">
                <section className="mq-hero">
                    <h1 className="mq-logo">MY<span>QUIZZES</span></h1>
                    <p className="mq-lead">Manage and test your creations.</p>
                </section>

                <section className="mq-list-section">
                    <MyQuizList
                        quizzes={state.myQuizzes}
                        loading={state.loading}
                        error={state.error}
                        onPlay={actions.playSolo}
                        onDelete={actions.deleteQuiz}
                    />
                </section>
            </main>
        </div>
    );
}