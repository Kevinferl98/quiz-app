import "../../styles/soloQuiz/QuizFooter.css";

interface Props {
  score: number;
  total: number;
}

export function QuizFooter({ score, total }: Props) {
  return (
    <footer className="mq-quiz-stats-footer">
      <div className="mq-score-pill">
        Current Score: <strong>{score}</strong> <span className="mq-divider">/</span> {total}
      </div>
    </footer>
  );
}