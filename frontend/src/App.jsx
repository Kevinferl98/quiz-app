import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import QuizListPage from "./pages/QuizListPage";
import QuizPage from "./pages/QuizPage";
import ResultPage from "./pages/ResultPage";
import CreateQuiz from "./pages/CreateQuiz";
import { Authenticator } from "@aws-amplify/ui-react";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />

        <Route
          path="/quizzes"
          element={
            <Authenticator hideSignUp components={{ SignIn: { Footer: () => null } }}>
              <QuizListPage />
            </Authenticator>
          }
        />
        <Route
          path="/quiz/:id"
          element={
            <Authenticator hideSignUp components={{ SignIn: { Footer: () => null } }}>
              <QuizPage />
            </Authenticator>
          }
        />
        <Route
          path="/results"
          element={
            <Authenticator hideSignUp components={{ SignIn: { Footer: () => null } }}>
              <ResultPage />
            </Authenticator>
          }
        />
        <Route
          path="/create"
          element={
            <Authenticator hideSignUp components={{ SignIn: { Footer: () => null } }}>
              <CreateQuiz />
            </Authenticator>
          }
        />
      </Routes>
    </Router>
  );
}