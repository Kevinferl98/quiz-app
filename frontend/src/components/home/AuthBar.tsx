import "../../styles/home/AuthBar.css"

export function AuthBar({ authenticated, username, onLogin, onLogout }: any) {
    return (
        <div className="auth-bar">
            {!authenticated ? (
                <button className="primary-btn" onClick={onLogin}>Login / Sign Up</button>
            ) : (
                <>
                    <span>Welcome {username}</span>
                    <button className="primary-btn" onClick={onLogout}>Logout</button>
                </>
            )}
        </div>
    );
}