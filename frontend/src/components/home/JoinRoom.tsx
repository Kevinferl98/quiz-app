export function JoinRoom({ roomCode, onChange, onJoin }: any) {
    return (
        <div className="join-room">
            <input
                type="text"
                placeholder="Enter room code"
                value={roomCode}
                onChange={(e) => onChange(e.target.value)}
            />
            <button onClick={onJoin}>Join Room</button>
        </div>
    );
}