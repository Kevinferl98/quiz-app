import "../../styles/createQuiz/QuizForm.css"

interface Question {
  text: string;
  options: string[];
  correctIndex: number;
}

interface Props {
  title: string;
  questions: Question[];
  onTitleChange: (value: string) => void;
  onAddQuestion: () => void;
  onQuestionChange: (index: number, value: string) => void;
  onOptionChange: (qIndex: number, optIndex: number, value: string) => void;
  onCorrectChange: (qIndex: number, idx: number) => void;
}

export function QuizForm({
    title,
    questions,
    onTitleChange,
    onAddQuestion,
    onQuestionChange,
    onOptionChange,
    onCorrectChange
}: Props) {
    return (
        <>
            <input
                className="title-input"
                type="text"
                placeholder="Quiz Title"
                value={title}
                onChange={(e) => onTitleChange(e.target.value)} 
            />

            <button className="add-question-button" onClick={onAddQuestion}>
                Add Question
            </button>

            {questions.map((q, qIdx) => (
                <div key={qIdx} className="question-card">
                    <input
                        className="question-input"
                        type="text"
                        placeholder={`Question ${qIdx + 1}`}
                        value={q.text}
                        onChange={(e) => onQuestionChange(qIdx, e.target.value)}
                    />

                    {q.options.map((opt, idx) => (
                        <div key={idx} className="option-row">
                            <input
                                type="radio"
                                checked={q.correctIndex === idx}
                                onChange={() => onCorrectChange(qIdx, idx)}
                            />

                            <input
                                className="option-input"
                                type="text"
                                value={opt}
                                placeholder={`Option ${idx + 1}`}
                                onChange={(e) => onOptionChange(qIdx, idx, e.target.value)}
                            />
                        </div>
                    ))}
                </div>
            ))}
        </>
    );
}