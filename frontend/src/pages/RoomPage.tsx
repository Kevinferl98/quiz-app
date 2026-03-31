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
        nameInput, nameSubmitted, selectedAnswer,
        correctAnswer, isFinalLeaderboard, totalTime, authenticated, viewState
    } = state;

    const renderContent = () => {
        switch (viewState) {
            case "ENTER_NAME":
                return (
                    <>
                        <h2>Enter your name to join</h2>
                        <input
                            type="text"
                            placeholder="Your name"
                            value={nameInput}
                            onChange={(e) =>
                                actions.setNameInput(e.target.value)
                            }
                        />
                        <button
                            className="primary-btn"
                            onClick={actions.handleSubmitName}
                        >
                            Join Room
                        </button>
                    </>
                );

            case "WAITING":
                return (
                    <WaitingRoom
                        players={players}
                        role={role}
                        onStart={actions.handleStart}
                    />
                );

            case "QUESTION":
                return (
                    <QuestionBox
                        question={question}
                        timer={timer}
                        totalTime={totalTime}
                        selectedAnswer={selectedAnswer}
                        correctAnswer={correctAnswer}
                        onAnswer={actions.handleAnswer}
                    />
                );

            case "LEADERBOARD":
                return (
                    <LeaderboardView
                        leaderboard={leaderboard}
                        isFinal={false}
                    />
                );

            case "FINISHED":
                return (
                    <>
                        <LeaderboardView
                            leaderboard={leaderboard}
                            isFinal={true}
                        />
                        <h2 className="game-ended-title">Game Finished!</h2>
                    </>
                );

            default:
                return null;
        }
    };

    return (
        <div className="room-container">
            <TopBar roomId={room_id} onBack={actions.disconnectAndGoHome} />

            {renderContent()}
        </div>
    )
}