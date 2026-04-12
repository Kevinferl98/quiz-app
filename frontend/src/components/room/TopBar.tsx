import "../../styles/room/TopBar.css";

interface TopBarProps {
    roomId: string | undefined;
    onBack: () => void;
}

export function TopBar({ roomId, onBack }: TopBarProps) {
    return (
        <header className="mq-room-topbar">
            <button className="mq-btn-back-minimal" onClick={onBack}>
                ← Back to Dashboard
            </button>
            <div className="mq-room-badge">
                <span className="mq-badge-label">ROOM CODE</span>
                <span className="mq-badge-value">{roomId}</span>
            </div>
        </header>
    );
}