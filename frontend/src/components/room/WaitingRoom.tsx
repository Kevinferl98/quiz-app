import "../../styles/room/WaitingRoom.css";

interface WaitingRoomProps {
    players: string[];
    role: "host" | "player";
    onStart: () => void;
}

export function WaitingRoom({ players, role, onStart }: WaitingRoomProps) {
    return (
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
                        <div className="online-dot" />
                    </div>
                ))}
            </div>

            {role === "host" && (
                <button 
                    className="primary-btn start-btn big-start" 
                    onClick={onStart}
                >
                    Start Quiz
                </button>
            )}
        </div>
    );
}