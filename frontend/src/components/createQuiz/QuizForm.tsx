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
        <div className="mq-form-container">
            <section className="mq-form-section">
                <label className="mq-label">Quiz Title</label>
                <input
                    className="mq-input-title"
                    type="text"
                    placeholder="Example: General Knowledge 2026"
                    value={title}
                    onChange={(e) => onTitleChange(e.target.value)} 
                />
            </section>

            <div className="mq-section-header">
                <h2 className="mq-section-title">Questions</h2>
                <button className="mq-btn-add" onClick={onAddQuestion}>
                    <span>+</span> Add Question
                </button>
            </div>

            <div className="mq-questions-list">
                {questions.map((q, qIdx) => (
                    <div key={qIdx} className="mq-question-card">
                        <div className="mq-question-header">
                            <span className="mq-question-number">#{qIdx + 1}</span>
                            <input
                                className="mq-input-question"
                                type="text"
                                placeholder="Enter your question here..."
                                value={q.text}
                                onChange={(e) => onQuestionChange(qIdx, e.target.value)}
                            />
                        </div>

                        <div className="mq-options-grid">
                            {q.options.map((opt, idx) => (
                                <div key={idx} className={`mq-option-item ${q.correctIndex === idx ? 'is-correct' : ''}`}>
                                    <label className="mq-radio-container">
                                        <input
                                            type="radio"
                                            name={`correct-${qIdx}`}
                                            checked={q.correctIndex === idx}
                                            onChange={() => onCorrectChange(qIdx, idx)}
                                        />
                                        <span className="mq-checkmark"></span>
                                    </label>
                                    <input
                                        className="mq-input-option"
                                        type="text"
                                        value={opt}
                                        placeholder={`Option ${idx + 1}`}
                                        onChange={(e) => onOptionChange(qIdx, idx, e.target.value)}
                                    />
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}