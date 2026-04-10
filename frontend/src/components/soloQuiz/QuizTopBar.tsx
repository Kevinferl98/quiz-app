import "../../styles/soloQuiz/QuizTopBar.css";

interface Props {
  title: string;
  onBack: () => void;
}

export function QuizTopBar({ title, onBack }: Props) {
  return (
    <header className="quiz-topbar">
      <button className="primary-btn" onClick={onBack}>
        ← Back
      </button>

      <h1 className="quiz-title">{title}</h1>

      <div style={{ width: 75 }}></div>
    </header>
  );
}