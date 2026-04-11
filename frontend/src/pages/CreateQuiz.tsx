import { useCreateQuiz } from "../hooks/useCreateQuiz";
import { QuizForm } from "../components/createQuiz/QuizForm";
import { ActionsButtons } from "../components/createQuiz/ActionsButtons";
import "../styles/createQuiz/CreateQuiz.css";

export default function CreateQuiz() {
  const { state, actions } = useCreateQuiz();

  return (
    <div className="mq-container">
      <header className="mq-hero">
        <h1 className="mq-logo">CREATE<span>QUIZ</span></h1>
        <p className="mq-lead">Design your challenge and share it with the world.</p>
      </header>

      <main className="mq-create-wrapper">
        <QuizForm
          title={state.title}
          questions={state.questions}
          onTitleChange={actions.setTitle}
          onAddQuestion={actions.addQuestion}
          onQuestionChange={actions.updateQuestionText}
          onOptionChange={actions.updateOption}
          onCorrectChange={actions.setCorrectOption}
        />      

        <ActionsButtons
          onSubmit={actions.submit}
          onCancel={actions.goHome}
          disabled={!state.isValid}
        />
      </main>
    </div>
  );
}