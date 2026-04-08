export function AuthBar({ authenticated, username, onLogin, onLogout }: any) {
    return (
        <div className="auth-bar">
            {!authenticated ? (
                <button onClick={onLogin}>Login / Sign Up</button>
            ) : (
                <>
                    <span>Welcome {username}</span>
                    <button onClick={onLogout}>Logout</button>
                </>
            )}
        </div>
    );
}