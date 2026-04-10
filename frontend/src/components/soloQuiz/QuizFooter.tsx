import "../../styles/soloQuiz/QuizFooter.css";

interface Props {
  score: number;
  total: number;
}

export function QuizFooter({ score, total }: Props) {
  return (
    <footer className="quiz-footer">
      <p>
        Score: {score} / {total}
      </p>
    </footer>
  );
}