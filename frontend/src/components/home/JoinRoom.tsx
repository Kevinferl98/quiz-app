import "../../styles/home/JoinRoom.css";

export function JoinRoom({ roomCode, onChange, onJoin }: any) {
    return (
        <div className="mq-join-card">
            <div className="mq-input-group">
                <input
                    className="mq-input-main"
                    type="text"
                    placeholder="Room code"
                    value={roomCode}
                    onChange={(e) => onChange(e.target.value)}
                />
                <button className="mq-btn-primary" onClick={onJoin}>Join Room</button>
            </div>
        </div>
    );
}