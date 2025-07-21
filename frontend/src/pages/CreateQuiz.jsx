import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/CreateQuiz.css";

export default function CreateQuiz() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState([]);

  const handleAddQuestion = () => {
    setQuestions([
      ...questions,
      { text: "", options: ["", "", "", ""], correctIndex: 0 },
    ]);
  };

  const handleQuestionChange = (index, field, value) => {
    const updated = [...questions];
    updated[index][field] = value;
    setQuestions(updated);
  };

  const handleOptionChange = (qIndex, optIndex, value) => {
    const updated = [...questions];
    updated[qIndex].options[optIndex] = value;
    setQuestions(updated);
  };

  const handleCorrectChange = (qIndex, idx) => {
    const updated = [...questions];
    updated[qIndex].correctIndex = idx;
    setQuestions(updated);
  };

  const handleSubmit = () => {
    const quizData = { title, questions };
    console.log("Quiz to submit:", quizData);
    // TODO
    navigate("/quizzes");
  };

  return (
    <div className="create-quiz-container">
      <h1>Create New Quiz</h1>

      <input type="text" placeholder="Quiz Title" value={title} onChange={(e) => setTitle(e.target.value)} className="title-input"/>

      <button onClick={handleAddQuestion} className="add-question-button">Add Question</button>

      {questions.map((q, qIdx) => (
        <div key={qIdx} className="question-card">
          <input type="text" placeholder={`Question ${qIdx + 1}`} value={q.text} onChange={(e) => handleQuestionChange(qIdx, "text", e.target.value)} className="question-input"/>
          {q.options.map((opt, idx) => (
            <div key={idx} className="option-row">
              <input type="radio" checked={q.correctIndex === idx} onChange={() => handleCorrectChange(qIdx, idx)}/>
              <input type="text" value={opt} placeholder={`Option ${idx + 1}`} onChange={(e) => handleOptionChange(qIdx, idx, e.target.value)} className="option-input"/>
            </div>
          ))}
        </div>
      ))}

      <div className="action-buttons">
        <button onClick={handleSubmit} className="submit-button">Create</button>
        <button onClick={() => navigate("/quizzes")} className="cancel-button">Cancel</button>
      </div>
    </div>
  );
}