import "../../styles/room/TopBar.css";

interface TopBarProps {
    roomId: string | undefined;
    onBack: () => void;
}

export function TopBar({ roomId, onBack }: TopBarProps) {
    return (
        <div className="top-bar">
            <button className="primary-btn" onClick={onBack}>
                Back to Home
            </button>
            <div className="room-id-box">
                <span className="room-id-label">Room Code</span>
                <span className="room-id-value">{roomId}</span>
            </div>
        </div>
    );
}