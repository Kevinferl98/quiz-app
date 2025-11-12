import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/QuizPage.css";
import {apiFetch} from "../api/api";

export default function QuizPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    async function fetchQuiz() {
        setLoading(true);
        setError(null);
        try{
            const data = await apiFetch(`/quizzes/${id}`);
            setQuiz(data);
        } catch (err) {
            setError(err.message || "Failed to load quiz");
        } finally {
            setLoading(false);
        }
    }
    fetchQuiz();
  }, [id]);

  const handleBack = () => navigate("/quizzes");

  const handleOptionSelect = (questionId, option) => {
    setAnswers((prev) => ({ ...prev, [questionId]: option }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length != quiz.questions.length) {
        alert("Please answer all questions before submitting.");
        return;
    }

    try {
        const result = await apiFetch("/saveResult", {
          method: "POST",
          body: JSON.stringify({ quizId: quiz.id, answers })
        }, true);
        
        alert(`Results: ${JSON.stringify(result)}`);
        navigate("/quizzes");
    } catch (err) {
        console.error("Error submitting answers:", err);
        alert("Error submitting quiz: " + (err.message || "Unknown error"));
    }
  };

  const renderHeader = (title) => {
    return (
      <header className="quiz-topbar">
        <button className="back-button" onClick={handleBack}>← Back</button>
        <h1 className="quiz-title">{title}</h1>
        <div style={{width: 75}}></div>
      </header>
    )
  };

  if (loading) return (
    <div className="quiz-container">
        {renderHeader("Loading quiz...")}
        <main className="questions-container"></main>
    </div>
  );

  if (error) return (
    <div className="quiz-container">
        {renderHeader(`Error: ${error}`)}
        <main className="questions-container"></main>
    </div>
  )

  if (!quiz) return (
    <div className="quiz-container">
        {renderHeader("Quiz Not Found")}
        <main className="questions-container"></main>
    </div>
  )

  return (
    <div className="quiz-container">
        {renderHeader(quiz.title)}

      <main className="questions-container">
        {quiz.questions.map((q) => (
          <div key={q.id} className="question-block">
            <p className="question-text">{q.question_text}</p>
            <div className="options-container">
              {q.options.map((option, idx) => (
                <label key={idx} className="option-label">
                  <input type="radio" name={`question-${q.id}`} checked={answers[q.id] === option} onChange={() => handleOptionSelect(q.id, option)}/>
                  <span className="custom-radio" />
                  {option}
                </label>
              ))}
            </div>
          </div>
        ))}
      </main>

      <footer className="quiz-footer">
        <button className="submit-button" onClick={handleSubmit} disabled={Object.keys(answers).length !== quiz.questions.length} title={
            Object.keys(answers).length !== quiz.questions.length
              ? "Please answer all questions"
              : "Submit your answers"
          }
        >
          Submit
        </button>
      </footer>
    </div>
  );
}