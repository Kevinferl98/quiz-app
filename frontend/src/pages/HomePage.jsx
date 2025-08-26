import "../styles/HomePage.css";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import { signIn } from 'aws-amplify/auth'

export default function HomePage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);
    try {
      await signIn({
        username: username,
        password: password
      });
      navigate("/quizzes");
    } catch (err) {
      setErrorMsg(err.message || "Error during login");
    } finally {
      setLoading(false);
    }
  };

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
          <button type="submit" className="button" disabled={loading}>
            {loading ? "Loading..." : "Login"}
          </button>
          {errorMsg && <div className="error">{errorMsg}</div>}
        </form>
      </div>
    </div>
  );
}