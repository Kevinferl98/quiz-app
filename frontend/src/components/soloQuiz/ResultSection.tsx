import "../../styles/soloQuiz/ResultSection.css";

interface Props {
  isCorrect: boolean | null;
  isLast: boolean;
  onNext: () => void;
}

export function ResultSection({ isCorrect, isLast, onNext }: Props) {
  return (
    <div className={`mq-result-banner ${isCorrect ? 'success' : 'error'}`}>
      <div className="mq-result-content">
        <div className="mq-result-text">
            <span className="mq-result-icon">{isCorrect ? '✨' : '⚠️'}</span>
            <p>{isCorrect ? "Correct Answer!" : "Oops, that wasn't correct!"}</p>
        </div>
        <button className="mq-btn-next" onClick={onNext}>
          {isLast ? "View Results" : "Next Question"}
        </button>
      </div>
    </div>
  );
}