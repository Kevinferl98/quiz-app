import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/SoloQuizPage.css";
import { apiFetch } from "../api/api"

interface Question {
    id: string;
    question_text: string;
    options: string[];
}

interface Quiz {
    quizId: string;
    title: string;
    questions: Question[];
}

export default function SoloQuizPage() {
    const { id } = useParams<{ id: string}>();
    const navigate = useNavigate();

    const [quiz, setQuiz] = useState<Quiz | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [currentIndex, setCurrentIndex] = useState(0);
    const [selectedOption, setSelectedOption] = useState<string | null>(null);
    const [showResult, setShowResult] = useState(false);
    const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
    const [score, setScore] = useState(0);

    useEffect(() => {
        async function fetchQuiz() {
            if (!id) return;

            setLoading(true);
            setError(null);

            try {
                const data: Quiz = await apiFetch(`http://quiz-service:8080/quizzes/${id}`);
                setQuiz(data);
            } catch (err: any) {
                setError(err.message || "Failed to laod quiz");
            } finally {
                setLoading(false);
            }
        }

        fetchQuiz();
    }, [id]);

    const handleBack = () => navigate("/");

    if (loading) return <div className="quiz-container"><h2>Loading quiz...</h2></div>
    if (error || !quiz)
        return (
            <div className="quiz-container">
                <h2>{error || "Quiz not found"}</h2>
                <button onClick={handleBack}>Back</button>
            </div>
        );

    const currentQuestion = quiz.questions[currentIndex];

    const handleOptionClick = async (option: string) => {
        if (showResult) return;
        setSelectedOption(option);

        try {
            const result: { correct: boolean} = await apiFetch(
                `http://quiz-service:8080/quizzes/${quiz.quizId}/answer`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        question_id: currentQuestion.id,
                        answer: option
                    })
                }
            );

            setIsCorrect(result.correct);
            setShowResult(true);

            if (result.correct) setScore((prev) => prev + 1);
        } catch (err) {
            alert("Error checking answer");
        }
    };

    const handleNext = () => {
        setSelectedOption(null);
        setShowResult(false);
        setIsCorrect(null);

        if (currentIndex < quiz.questions.length - 1) {
            setCurrentIndex((prev) => prev + 1);
        } else {
            alert(`Quiz finished! Score: ${score}/${quiz.questions.length}`);
            navigate("/");
        }
    };

    return (
        <div className="quiz-container">
            <header className="quiz-topbar">
                <button className="back-button" onClick={handleBack}>← Back</button>
                <h1 className="quiz-title">{quiz.title}</h1>
                <div style={{ width: 75 }}></div>
            </header>

            <main className="questions-container">
                <div className="question-block">
                    <p className="question-counter">
                        Question {currentIndex + 1} / {quiz.questions.length}
                    </p>

                    <p className="question-text">{currentQuestion.question_text}</p>

                    <div className="options-container">
                        {currentQuestion.options.map((option, idx) => {
                            let className = "option-button";
                            if (showResult) {
                                if (option == selectedOption) {
                                    className += isCorrect ? "correct" : "wrong";
                                }
                            }

                            return (
                                <button key={idx} className={className} onClick={() => handleOptionClick(option)} disabled={showResult}>{option}</button>
                            );
                        })}
                    </div>

                    {showResult && (
                        <div className="result-section">
                            <p>
                                {isCorrect ? "Correct!" : "Wrong!"}
                            </p>
                            <button className="next-button" onClick={handleNext}>
                               {currentIndex < quiz.questions.length - 1 ? "Continue" : "Finish"}
                            </button>
                        </div>
                    )}
                </div>
            </main>

            <footer className="quiz-footer">
                <p>Score: {score} / {quiz.questions.length}</p>
            </footer>
        </div>
    );
}