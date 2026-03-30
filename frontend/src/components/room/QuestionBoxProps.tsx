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
        <div className="question-box">
            <div className="question-header">
                <h2 className="question-text">{question.question_text}</h2>
            </div>
            
            <div className="timer-container">
                <div className="timer-bar" style={{ width: `${progress}%` }} />
                <div className="timer-text">{timer}s</div>
            </div>

            <div className="options">
                {question.options.map((opt: string, i: number) => {
                    let className = "option-btn";

                    if (selectedAnswer === opt) className += " selected";
                    if (correctAnswer) {
                        if (opt === correctAnswer) className += " correct";
                        else if (opt === selectedAnswer) className += " wrong";
                    }

                    return (
                        <button
                            key={i}
                            className={className}
                            onClick={() => onAnswer(opt)}
                            disabled={!!selectedAnswer}
                        >
                            {opt}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}