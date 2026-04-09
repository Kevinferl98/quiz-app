import "../../styles/home/Pagination.css";

export function Pagination({ page, pages, onChange }: any) {
    return (
        <div className="pagination">
            {Array.from({ length: pages }, (_, i) => i + 1).map((p) => (
                <button
                    key={p}
                    onClick={() => onChange(p)}
                    className={`primary-btn ${p === page ? "active" : ""}`}
                >
                    {p}
                </button>
            ))}
        </div>
    );
}