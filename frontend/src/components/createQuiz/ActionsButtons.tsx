import "../../styles/createQuiz/ActionsButtons.css"

interface Props {
  onSubmit: () => void;
  onCancel: () => void;
  disabled: boolean;
}

export function ActionsButtons({
    onSubmit,
    onCancel,
    disabled
}: Props) {
    return (
        <div className="action-buttons">
            <button
                className="primary-btn"
                onClick={onSubmit}
                disabled={disabled}
                title={disabled ? "Fill all fields before submitting" : "Create quiz"}
            >
                Create
            </button>

            <button className="primary-btn cancel-btn" onClick={onCancel}>
                Cancel
            </button>
        </div>
    );
}