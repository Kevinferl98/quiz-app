interface LeaderboardEntry {
    name: string;
    score: number;
}

interface LeaderboardViewProps {
    leaderboard: LeaderboardEntry[];
    isFinal: boolean;
}

export function LeaderboardView({ leaderboard, isFinal }: LeaderboardViewProps) {
    if (leaderboard.length === 0) return null;

    return (
        <div className="leaderboard-box">
            <h2 className="leaderboard-title">
                {isFinal ? "Final Results" : "Leaderboard"}
            </h2>

            <div className="podium">
                {leaderboard[1] && (
                    <div className="podium-item second">
                        <div className="podium-name">{leaderboard[1].name}</div>
                        <div className="podium-score">{leaderboard[1].score}</div>
                    </div>
                )}

                {leaderboard[0] && (
                    <div className="podium-item first">
                        <div className="podium-name">{leaderboard[0].name}</div>
                        <div className="podium-score">{leaderboard[0].score}</div>
                    </div>
                )}

                {leaderboard[2] && (
                    <div className="podium-item third">
                        <div className="podium-name">{leaderboard[2].name}</div>
                        <div className="podium-score">{leaderboard[2].score}</div>
                    </div>
                )}
            </div>

            <div className="leaderboard-list">
                {leaderboard.slice(3).map((entry, i) => (
                    <div key={i} className="leaderboard-row">
                        <span>#{i + 4}</span>
                        <span>{entry.name}</span>
                        <span>{entry.score}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}