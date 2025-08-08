import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/ResultPage.css";

export default function ResultPage() {
  const navigate = useNavigate();

  const [results, setResults] = useState([]);
  
  useEffect(() => {
    setResults([
      {id: 1, title: "Lorem Ipsum", score: "2/3"},
      {id: 2, title: "Lorem Ipsum", score: "3/5"},
      {id: 3, title: "Lorem Ipsum", score: "5/5"}
    ]);
  }, []);

  const handleBack = () => {
    navigate("/quizzes");
  };

  return (
    <div className="results-container">
      <header className="results-topbar">
        <button className="back-button" onClick={handleBack}>← Back</button>
        <h1 className="results-title">Your Results</h1>
        <div style={{width: 75}}></div>
      </header>

      <main className="results-list">
        {results.length === 0 ? (
          <p className="no-results">No results found.</p>) : (
            <ul>
              {results.map((result) => (
                <li key={result.id} className="result-item">
                  <span className="result-title">{result.title}</span>
                  <span className="result-score">{result.score}</span>
                </li>
              ))}
            </ul>
          )}
      </main>
    </div>
  );
}