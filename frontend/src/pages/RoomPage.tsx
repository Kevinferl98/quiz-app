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
        nameInput, selectedAnswer,
        correctAnswer, totalTime, viewState
    } = state;

    const renderContent = () => {
        switch (viewState) {
            case "ENTER_NAME":
                return (
                    <div className="mq-join-container">
                        <div className="mq-join-card-static">
                            <h2 className="mq-section-title-center">Join the Challenge</h2>
                            <p className="mq-text-muted-center">Enter your nickname to enter the room</p>
                            <input
                                className="mq-input-join"
                                type="text"
                                placeholder="Your Awesome Nickname"
                                value={nameInput}
                                onChange={(e) => actions.setNameInput(e.target.value)}
                            />
                            <button className="mq-btn-primary-full" onClick={actions.handleSubmitName}>
                                Join Room
                            </button>
                        </div>
                    </div>
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
                    <div className="mq-finished-container">
                        <LeaderboardView
                            leaderboard={leaderboard}
                            isFinal={true}
                        />
                        <div className="mq-end-actions">
                             <h2 className="mq-game-ended-text">The Game has Finished!</h2>
                             <button className="mq-btn-outline-full" onClick={actions.disconnectAndGoHome}>Return to Dashboard</button>
                        </div>
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div className="mq-room-layout">
            <TopBar roomId={room_id} onBack={actions.disconnectAndGoHome} />
            <main className="mq-room-main-content">
                {renderContent()}
            </main>
        </div>
    )
}