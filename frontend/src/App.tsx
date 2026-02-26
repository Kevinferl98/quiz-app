import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CreateQuiz from "./pages/CreateQuiz";
import SoloQuizPage from "./pages/SoloQuizPage";
import MyQuizzesPage from "./pages/MyQuizzesPage";
import CreateGameRoom from "./pages/CreateGameRoom";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/solo-quiz/:id" element={<SoloQuizPage />} />
        <Route path="/create" element={<CreateQuiz />} />
        <Route path="/my-quizzes" element={<MyQuizzesPage />} />
        <Route path="/create-room" element={<CreateGameRoom />} />
      </Routes>
    </Router>
  );
}