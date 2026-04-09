import { useHomePage } from "../hooks/useHomePage";
import { AuthBar } from "../components/home/AuthBar";
import { JoinRoom } from "../components/home/JoinRoom";
import { MainActions } from "../components/home/MainActions";
import { QuizList } from "../components/home/QuizList";
import { Pagination } from "../components/home/Pagination";
import "../styles/home/HomePage.css";

export default function HomePage() {
  const { state, actions } = useHomePage();

  return (
    <div className="home-container">
      <AuthBar
        authenticated={state.authenticated}
        username={state.username}
        onLogin={actions.login}
        onLogout={actions.logout}
      />

      <h1>Quiz App</h1>

      <JoinRoom
        roomCode={state.roomCode}
        onChange={actions.setRoomCode}
        onJoin={actions.joinRoom}
      />

      <MainActions
        authenticated={state.authenticated}
        onCreateQuiz={actions.createQuiz}
        onCreateRoom={actions.createRoom}
        onMyQuizzes={actions.goToMyQuizzes}
      />

      <QuizList
        quizzes={state.quizzes}
        loading={state.loading}
        error={state.error}
        onPlay={actions.playSolo}
      />

      <Pagination
        page={state.page}
        pages={state.pages}
        onChange={actions.setPage}
      />
    </div>
  );
}
