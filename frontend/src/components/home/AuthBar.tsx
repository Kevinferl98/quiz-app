import "../../styles/home/AuthBar.css"

export function AuthBar({ authenticated, username, onLogin, onLogout }: any) {
    return (
        <div className="mq-auth-bar">
            {!authenticated ? (
                <button className="mq-btn-outline" onClick={onLogin}>Login</button>
            ) : (
                <div className="mq-user-pill">
                    <span className="mq-username">Hi, <strong>{username}</strong></span>
                    <button className="mq-btn-danger-sm" onClick={onLogout}>Logout</button>
                </div>
            )}
        </div>
    );
}