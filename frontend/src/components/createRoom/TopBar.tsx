import "../../styles/createRoom/TopBar.css"

interface Props {
    onBack: () => void;
    onLogout: () => void;
}

export function TopBar({ onBack, onLogout } : Props) {
    return (
        <div className="mq-top-bar">
            <button className="mq-btn-back" onClick={onBack}>
                <span className="mq-back-icon">←</span> Back to Home
            </button>

            <button className="mq-btn-danger-sm" onClick={onLogout}>
                Logout
            </button>
        </div>
    );
}