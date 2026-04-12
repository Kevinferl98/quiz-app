import "../../styles/myQuizzes/TopBar.css"

interface Props {
    username?: string;
    onBack: () => void;
    onLogout: () => void;
}

export function TopBar({ username, onBack, onLogout }: Props) {
    return (
        <div className="mq-top-bar">
            <button className="mq-btn-back-minimal" onClick={onBack}>
                <span className="mq-icon-sm">←</span> Home
            </button>

            <div className="mq-user-section">
                <div className="mq-user-info">
                    <span className="mq-welcome">Account: <strong>{username}</strong></span>
                </div>
                <button className="mq-btn-danger-sm" onClick={onLogout}>Logout</button>
            </div>
        </div>
    );
}