import { useSoloQuiz } from "../hooks/useSoloQuiz";
import { QuizTopBar } from "../components/soloQuiz/QuizTopBar";
import { QuestionCard } from "../components/soloQuiz/QuestionCard";
import { ResultSection } from "../components/soloQuiz/ResultSection";
import { QuizFooter } from "../components/soloQuiz/QuizFooter";
import "../styles/soloQuiz/SoloQuizPage.css";

export default function SoloQuizPage() {
    const { state, actions } = useSoloQuiz();

    if (state.loading)
        return (
            <div className="mq-container mq-flex-center">
                <div className="mq-loader"></div>
                <h2 className="mq-loading-text">Loading quiz...</h2>
            </div>
        );

    if (state.error || !state.quiz)
        return (
            <div className="mq-container mq-flex-center">
                <div className="mq-error-card">
                    <h2>Oops!</h2>
                    <p>{state.error || "Quiz not found"}</p>
                    <button className="mq-btn-primary" onClick={actions.goHome}>
                        Go back home
                    </button>
                </div>
            </div>
        );

    return (
        <div className="mq-quiz-layout">
            <QuizTopBar
                title={state.quiz.title}
                onBack={actions.goHome}
            />

            <main className="mq-quiz-main">
                <QuestionCard
                    question={state.currentQuestion!}
                    index={state.currentIndex}
                    total={state.quiz.questions.length}
                    selectedOption={state.selectedOption}
                    showResult={state.showResult}
                    isCorrect={state.isCorrect}
                    onSelect={actions.selectOption}
                />

                {state.showResult && (
                    <ResultSection
                        isCorrect={state.isCorrect}
                        isLast={state.currentIndex === state.quiz.questions.length - 1}
                        onNext={actions.next}
                    />
                )}
            </main>
            
            <QuizFooter
                score={state.score}
                total={state.quiz.questions.length}
            />
        </div>
    );
}