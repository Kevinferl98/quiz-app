import "../../styles/room/QuestionBox.css";

interface QuestionBoxProps {
    question: any;
    timer: number;
    totalTime: number;
    selectedAnswer: string | null;
    correctAnswer: string | null;
    onAnswer: (answer: string) => void;
}

export function QuestionBox({
    question,
    timer,
    totalTime,
    selectedAnswer,
    correctAnswer,
    onAnswer
}: QuestionBoxProps) {
    const progress = (timer / totalTime) * 100;

    return (
        <div className="mq-question-box-card">
            <div className="mq-question-header-row">
                 <h2 className="mq-question-text-live">{question.question_text}</h2>
            </div>
            
            <div className="mq-timer-wrapper">
                <div className="mq-timer-track">
                    <div className="mq-timer-fill" style={{ 
                        width: `${progress}%`,
                        transition: correctAnswer ? "none" : "width 1s linear" 
                    }} />
                </div>
                <div className="mq-timer-badge">{timer}s</div>
            </div>

            <div className="mq-options-grid-live">
                {question.options.map((opt: string, i: number) => {
                    let stateClass = "";
                    if (selectedAnswer === opt) stateClass = " is-selected";
                    if (correctAnswer) {
                        if (opt === correctAnswer) stateClass = " is-correct";
                        else if (opt === selectedAnswer) stateClass = " is-wrong";
                        else stateClass = " is-dimmed";
                    }

                    return (
                        <button
                            key={i}
                            className={`mq-option-btn-live${stateClass}`}
                            onClick={() => onAnswer(opt)}
                            disabled={!!selectedAnswer}
                        >
                            <span className="mq-option-index">{String.fromCharCode(65 + i)}</span>
                            {opt}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}