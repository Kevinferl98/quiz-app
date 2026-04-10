import "../../styles/home/JoinRoom.css";

export function JoinRoom({ roomCode, onChange, onJoin }: any) {
    return (
        <div className="join-room">
            <input
                className="main-input"
                type="text"
                placeholder="Enter room code"
                value={roomCode}
                onChange={(e) => onChange(e.target.value)}
            />
            <button className="primary-btn" onClick={onJoin}>Join Room</button>
        </div>
    );
}