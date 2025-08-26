import "../styles/HomePage.css";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import { signIn, confirmSignIn } from 'aws-amplify/auth'

export default function HomePage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [challenge, setChallenge] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);
    try {
      const { nextStep } = await signIn({
        username: username,
        password: password
      });
      console.log(nextStep);
      if (nextStep.signInStep === "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED") {
        setChallenge(true);
        return;
      }

      navigate("/quizzes");
    } catch (err) {
      setErrorMsg(err.message || "Error during login");
    } finally {
      setLoading(false);
    }
  };

  const handleNewPasswordSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);

    try {
      await confirmSignIn({
        challengeResponse: newPassword
      });
      navigate("/quizzes");
    } catch (err) {
      setErrorMsg(err.message || "Error during password update");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Login</h1>
        {!challenge ? (
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
        ) : (
          <form className="form" onSubmit={handleNewPasswordSubmit}>
            <input
              type="password"
              placeholder="New password"
              className="input"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <button type="submit" className="button" disabled={loading}>
              {loading ? "Updating..." : "Update password"}
            </button>
            {errorMsg && <div className="error">{errorMsg}</div>}
          </form>
        )}
      </div>
    </div>
  );
}