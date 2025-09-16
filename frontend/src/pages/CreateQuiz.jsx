import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/CreateQuiz.css";
import {apiFetch} from "../api/api";

export default function CreateQuiz() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState([]);

  const handleAddQuestion = () => {
    setQuestions(prev => [
      ...prev,
      { text: "", options: ["", "", "", ""], correctIndex: 0 },
    ]);
  };

  const handleQuestionChange = (index, field, value) => {
    setQuestions(prev => {
        const updated = [...prev];
        updated[index].text = value;
        return updated;
    });
  };

  const handleOptionChange = (qIndex, optIndex, value) => {
    setQuestions(prev => {
        const updated = [...prev];
        updated[qIndex].options[optIndex] = value;
        return updated;
    });
  };

  const handleCorrectChange = (qIndex, idx) => {
    setQuestions(prev => {
        const updated = [...prev];
        updated[qIndex].correctIndex = idx;
        return updated;
    })
  };

  const isValidQuiz = () => {
    if (!title.trim()) return false;
    if (questions.length === 0) return false;
    for (const q of questions) {
        if (!q.text.trim()) return false;
        if (q.options.some(opt => !opt.trim())) return false;
    }
    return true;
  };

  const handleSubmit = async () => {
    if (!isValidQuiz()) {
        alert("Please fill in the quiz title and all question fields.");
        return;
    }

    const formattedQuestions = questions.map((q, i) => ({
      id: `q${i + 1}`,
      question_text: q.text,
      options: q.options,
      correct_option: q.options[q.correctIndex]
    }));

    try {
      const data = await apiFetch("http://localhost:8080/quizzes", {
        method: "POST",
        body: JSON.stringify({title, questions: formattedQuestions})
      });
      
      console.log("Quiz created with ID: ", data.quizId);
      navigate("/quizzes");
    } catch (error) {
      console.error("Error: ", error);
      alert("Error creating quiz: " + error.message);
    }
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
        <button onClick={handleSubmit} className="submit-button" disabled={!isValidQuiz()} title={!isValidQuiz() ? "Fill all fields before submitting" : "Create quiz"}>Create</button>
        <button onClick={() => navigate("/quizzes")} className="cancel-button">Cancel</button>
      </div>
    </div>
  );
}