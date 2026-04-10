import "../../styles/myQuizzes/TopBar.css"

interface Props {
    username?: string;
    onBack: () => void;
    onLogout: () => void;
}

export function TopBar({ username, onBack, onLogout }: Props) {
    return (
        <div className="top-bar">
            <button className="primary-btn" onClick={onBack}>← Back to Home</button>

            <div className="auth-section">
                <span>Welcome {username}</span>
                <button className="primary-btn" onClick={onLogout}>Logout</button>
            </div>
        </div>
    );
}