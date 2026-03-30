import { useRoomLogic } from "../hooks/useRoomLogic";
import "../styles/RoomPage.css";

export default function RoomPage() {
    const { state, actions } = useRoomLogic();
    const {
        room_id, role, players, question, timer, leaderboard,
        gameEnded, nameInput, nameSubmitted, selectedAnswer,
        correctAnswer, isFinalLeaderboard, totalTime, authenticated
    } = state;

    const progress = (timer / totalTime) * 100;

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
            <div className="top-bar">
                <button className="primary-btn" onClick={actions.disconnectAndGoHome}>Back to Home</button>
                <div className="room-id-box">
                    <span className="room-id-label">Room Code</span>
                    <span className="room-id-value">{room_id}</span>
                </div>
            </div>

            {!question && !gameEnded && (
                <div className="waiting-room">
                    <h2 className="waiting-title">Waiting Room</h2>
                    <p className="waiting-subtitle">
                        {players.length} player{players.length !== 1 && "s"} joined
                    </p>

                    <div className="players-grid">
                        {players.map((p, i) => (
                            <div key={i} className="player-card">
                                <div className="player-avatar">
                                    {p.charAt(0).toUpperCase()}
                                </div>

                                <div className="player-info">
                                    <span className="player-name">{p}</span>
                                    {role === "host" && i === 0 && (
                                        <span className="host-badge">HOST</span>
                                    )}
                                </div>

                                <div className="online-dot"/>
                            </div>
                        ))}
                    </div>
                    {role === "host" && (
                        <button className="primary-btn start-btn big-start" onClick={actions.handleStart}>Start Quiz</button>
                    )}
                </div>
            )}
            
            {question && (
                <div className="question-box">
                    <div className="question-header">
                        <h2 className="question-text">{question.question_text}</h2>
                    </div>
                    <div className="timer-container">
                        <div className="timer-bar" style={{ width: `${progress}%` }}/>
                        <div className="timer-text">{timer}s</div>
                    </div>
                    
                    <div className="options">
                        {question.options.map((opt: string, i: number) => {
                            let className = "option-btn";

                            if (selectedAnswer === opt) className += " selected";
                            if (correctAnswer) {
                                if (opt === correctAnswer) className += " correct";
                                else if (opt === selectedAnswer) className += " wrong";
                            }

                            return (
                                <button
                                    key={i}
                                    className={className}
                                    onClick={() => actions.handleAnswer(opt)}
                                    disabled={!!selectedAnswer}
                                >{opt}</button>
                            );
                        })}
                    </div>
                </div>
            )}

            {leaderboard.length > 0 && (
                <div className="leaderboard-box">
                    <h2 className="leaderboard-title">
                        {isFinalLeaderboard ? "Final Results" : "Leaderboard"}
                    </h2>

                    {/* PODIUM */}
                    <div className="podium">
                        {leaderboard[1] && (
                            <div className="podium-item second">
                                <div className="podium-name">{leaderboard[1].name}</div>
                                <div className="podium-score">{leaderboard[1].score}</div>
                            </div>
                        )}

                        {leaderboard[0] && (
                            <div className="podium-item first">
                                <div className="podium-name">{leaderboard[0].name}</div>
                                <div className="podium-score">{leaderboard[0].score}</div>
                            </div>
                        )}

                        {leaderboard[2] && (
                            <div className="podium-item third">
                                <div className="podium-name">{leaderboard[2].name}</div>
                                <div className="podium-score">{leaderboard[2].score}</div>
                            </div>
                        )}
                    </div>

                    <div className="leaderboard-list">
                        {leaderboard.slice(3).map((entry, i) => (
                            <div key={i} className="leaderboard-row">
                                <span>#{i + 4}</span>
                                <span>{entry.name}</span>
                                <span>{entry.score}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {gameEnded && <h2 className="game-ended-title">Game Finished!</h2>}
        </div>
    )
}