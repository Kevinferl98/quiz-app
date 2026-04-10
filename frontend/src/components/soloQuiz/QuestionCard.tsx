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
    <div className="question-block">
      <p className="question-counter">
        Question {index + 1} / {total}
      </p>

      <p className="question-text">
        {question.question_text}
      </p>

      <div className="options-container">
        {question.options.map((option, idx) => {
          let className = "option-button";

          if (showResult && option === selectedOption) {
            className += isCorrect ? " correct" : " wrong";
          }

          return (
            <button
              key={idx}
              className={className}
              onClick={() => onSelect(option)}
              disabled={showResult}
            >
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
}