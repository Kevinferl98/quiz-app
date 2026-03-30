import { useRoomLogic } from "../hooks/useRoomLogic";
import { TopBar } from "../components/room/TopBar";
import { WaitingRoom } from "../components/room/WaitingRoom";
import { QuestionBox } from "../components/room/QuestionBoxProps";
import { LeaderboardView } from "../components/room/LeaderboardView";
import "../styles/room/RoomPage.css";

export default function RoomPage() {
    const { state, actions } = useRoomLogic();
    const {
        room_id, role, players, question, timer, leaderboard,
        gameEnded, nameInput, nameSubmitted, selectedAnswer,
        correctAnswer, isFinalLeaderboard, totalTime, authenticated
    } = state;

    if (!authenticated && !nameSubmitted) {
        return (
            <div className="room-container">
                <h2>Enter your name to join</h2>
                <input
                    type="text"
                    placeholder="Your name"
                    value={nameInput}
                    onChange={(e) => actions.setNameInput(e.target.value)} 
                />
                <button className="primary-btn" onClick={actions.handleSubmitName}>Join Room</button>
            </div>
        );
    }

    return (
        <div className="room-container">
            <TopBar roomId={room_id} onBack={actions.disconnectAndGoHome} />

            {!question && !gameEnded && (
                <WaitingRoom
                    players={players}
                    role={role}
                    onStart={actions.handleStart}
                />
            )}
            
            {question && (
                <QuestionBox
                    question={question}
                    timer={timer}
                    totalTime={totalTime}
                    selectedAnswer={selectedAnswer}
                    correctAnswer={correctAnswer}
                    onAnswer={actions.handleAnswer}
                />
            )}

            {leaderboard.length > 0 && (
                <LeaderboardView
                    leaderboard={leaderboard}
                    isFinal={isFinalLeaderboard}
                />
            )}

            {gameEnded && <h2 className="game-ended-title">Game Finished!</h2>}
        </div>
    )
}