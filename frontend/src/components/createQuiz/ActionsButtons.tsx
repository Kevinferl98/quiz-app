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
        <div className="mq-actions-footer">
            <button className="mq-btn-secondary-lg" onClick={onCancel}>
                Cancel
            </button>
            
            <button
                className="mq-btn-primary-lg"
                onClick={onSubmit}
                disabled={disabled}
                title={disabled ? "Please fill in all fields before continuing" : "Create quiz"}
            >
                Crete Quiz
            </button>
        </div>
    );
}