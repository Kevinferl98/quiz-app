import { useCreateQuiz } from "../hooks/useCreateQuiz";
import { QuizForm } from "../components/createQuiz/QuizForm";
import { ActionsButtons } from "../components/createQuiz/ActionsButtons";
import "../styles/createQuiz/CreateQuiz.css";

export default function CreateQuiz() {
  const { state, actions } = useCreateQuiz();

  return (
    <div className="create-quiz-container">
      <h1>Create New Quiz</h1>

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
    </div>
  );
}