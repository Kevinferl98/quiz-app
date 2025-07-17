import "./HomePage.css";
import {useState} from "react";
import {useNavigate} from "react-router-dom";

export default function HomePage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/quizzes");
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Login</h1>
        <form className="form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            className="input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="button">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}