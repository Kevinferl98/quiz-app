import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ResultPage from "./pages/ResultPage";
import CreateQuiz from "./pages/CreateQuiz";
import SoloQuizPage from "./pages/SoloQuizPage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/solo-quiz/:id" element={<SoloQuizPage />} />
        <Route path="/results" element={<ResultPage />} />
        <Route path="/create" element={<CreateQuiz />} />
      </Routes>
    </Router>
  );
}