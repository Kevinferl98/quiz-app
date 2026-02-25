import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CreateQuiz from "./pages/CreateQuiz";
import SoloQuizPage from "./pages/SoloQuizPage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/solo-quiz/:id" element={<SoloQuizPage />} />
        <Route path="/create" element={<CreateQuiz />} />
      </Routes>
    </Router>
  );
}