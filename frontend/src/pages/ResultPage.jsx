import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "../styles/ResultPage.css";
import { apiFetch } from "../api/api";

export default function ResultPage() {
  const navigate = useNavigate();

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    async function loadResults() {
      setLoading(true);
      setError(null);
      try {
        const data = await apiFetch('/getResults', {}, true);
        const formatted = data.map((item, idx) => ({
          id: idx,
          title: item.quizTitle,
          score: item.score_percentage
        }));
        setResults(formatted);
      } catch (err) {
        console.error('Error fetching results:', err);
        setError(err.message || 'Failed to load results');
      } finally {
        setLoading(false);
      }
    }
    loadResults();
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
        {loading ? (
          <p>Loading results...</p>
        ) : error ? (
          <p className="no-results">Error: {error}</p>
        ) : results.length == 0 ? (
          <p className="no-results">No results found</p>
        ) : (
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