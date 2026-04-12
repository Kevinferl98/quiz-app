import "../../styles/soloQuiz/QuestionCard.css";

interface Question {
  question_text: string;
  options: string[];
}

interface Props {
  question: Question;
  index: number;
  total: number;
  selectedOption: string | null;
  showResult: boolean;
  isCorrect: boolean | null;
  onSelect: (option: string) => void;
}

export function QuestionCard({
  question,
  index,
  total,
  selectedOption,
  showResult,
  isCorrect,
  onSelect,
}: Props) {
  return (
    <div className="mq-question-container">
      <div className="mq-question-progress">
        <span className="mq-progress-text">Question {index + 1} of {total}</span>
        <div className="mq-progress-bar">
          <div 
            className="mq-progress-fill" 
            style={{ width: `${((index + 1) / total) * 100}%` }}
          ></div>
        </div>
      </div>

      <h2 className="mq-question-display">
        {question.question_text}
      </h2>

      <div className="mq-options-layout">
        {question.options.map((option, idx) => {
          let stateClass = "";
          if (showResult && option === selectedOption) {
            stateClass = isCorrect ? " is-correct" : " is-wrong";
          } else if (showResult && option !== selectedOption) {
            stateClass = " is-dimmed";
          } else if (option === selectedOption) {
            stateClass = " is-selected";
          }

          return (
            <button
              key={idx}
              className={`mq-option-btn${stateClass}`}
              onClick={() => onSelect(option)}
              disabled={showResult}
            >
              <span className="mq-option-letter">{String.fromCharCode(65 + idx)}</span>
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
}