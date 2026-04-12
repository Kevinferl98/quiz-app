import "../../styles/soloQuiz/QuizTopBar.css";

interface Props {
  title: string;
  onBack: () => void;
}

export function QuizTopBar({ title, onBack }: Props) {
  return (
    <header className="mq-quiz-top">
      <div className="mq-quiz-top-content">
        <button className="mq-btn-back-minimal" onClick={onBack}>
          <span className="mq-icon-sm">←</span> Back
        </button>
        <h1 className="mq-quiz-nav-title">{title}</h1>
        <div className="mq-top-spacer"></div>
      </div>
    </header>
  );
}