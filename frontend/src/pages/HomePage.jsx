import "./HomePage.css";

export default function HomePage() {
  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Login</h1>
        <form className="form">
          <input
            type="username"
            placeholder="Username"
            className="input"
          />
          <input
            type="password"
            placeholder="Password"
            className="input"
          />
          <button type="submit" className="button">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}