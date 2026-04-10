import { useCreateGameRoom } from "../hooks/useCreateGameRoom";
import { TopBar } from "../components/createRoom/TopBar";
import { QuizSelectionList } from "../components/createRoom/QuizSelectionList";

import "../styles/createRoom/CreateGameRoom.css";

export default function CreateGameRoom() {
    const { state, actions } = useCreateGameRoom();
    
    return (
        <div className="create-room-container">
            <TopBar
                onBack={actions.goHome}
                onLogout={actions.logout}
            />

            <h1>Create Game Room</h1>

            <QuizSelectionList
                quizzes={state.quizzes}
                loading={state.loading}
                error={state.error}
                creatingRoomId={state.creatingRoomId}
                onCreateRoom={actions.creteRoom}
            />
        </div>
    );
}