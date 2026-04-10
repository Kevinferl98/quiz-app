import "../../styles/soloQuiz/ResultSection.css";

interface Props {
  isCorrect: boolean | null;
  isLast: boolean;
  onNext: () => void;
}

export function ResultSection({
  isCorrect,
  isLast,
  onNext,
}: Props) {
  return (
    <div className="result-section">
      <p>{isCorrect ? "Correct!" : "Wrong!"}</p>

      <button className="primary-btn" onClick={onNext}>
        {isLast ? "Finish" : "Continue"}
      </button>
    </div>
  );
}