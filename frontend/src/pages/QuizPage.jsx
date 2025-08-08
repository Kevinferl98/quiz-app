import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import "../styles/QuizPage.css";

const quizzesData = {
  1: {
    title: "Lorem Ipsum Quiz",
    questions: [
      {
        id: 1,
        text: "Lorem Ipsum",
        options: [
          "Lorem Ipsum",
          "Lorem Ipsum",
          "Lorem Ipsum",
          "Lorem Ipsum",
        ],
      }
    ],
  },
};

export default function QuizPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const quiz = quizzesData[id];
  const [answers, setAnswers] = useState({});

  const handleBack = () => {
    navigate("/quizzes");
  };

  if (!quiz) {
    return (
      <div className="quiz-container">
        <header className="quiz-topbar">
          <button className="back-button" onClick={handleBack}>← Back</button>
          <h1 className="quiz-title">Quiz Not Found</h1>
          <div style={{ width: 75 }} />
        </header>
        <main className="questions-container"></main>
      </div>
    );
  }

  const handleOptionSelect = (questionId, optionIndex) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleSubmit = () => {
    // TODO
    alert("Submitted answers: " + JSON.stringify(answers));
    navigate("/quizzes")
  };

  return (
    <div className="quiz-container">
      <header className="quiz-topbar">
        <button className="back-button" onClick={handleBack}>← Back</button>
        <h1 className="quiz-title">{quiz.title}</h1>
        <div style={{ width: 75 }} /> {}
      </header>

      <main className="questions-container">
        {quiz.questions.map((q) => (
          <div key={q.id} className="question-block">
            <p className="question-text">{q.text}</p>
            <div className="options-container">
              {q.options.map((option, idx) => (
                <label key={idx} className="option-label">
                  <input type="radio" name={`question-${q.id}`} checked={answers[q.id] === idx} onChange={() => handleOptionSelect(q.id, idx)}/>
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