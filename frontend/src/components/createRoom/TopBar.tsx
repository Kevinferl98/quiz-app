
import "../../styles/createRoom/TopBar.css"

interface Props {
    onBack: () => void;
    onLogout: () => void;
}

export function TopBar({ onBack, onLogout } : Props) {
    return (
        <div className="top-bar">
            <button className="primary-btn" onClick={onBack}>
                ← Back to Home
            </button>

            <button className="primary-btn" onClick={onLogout}>
                Logout
            </button>
        </div>
    );
}