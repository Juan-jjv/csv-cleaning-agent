import { useState } from "react";


const AVAILABLE_ACTIONS = [
    {
        label: "Remove duplicates",
        instruction: "Remove duplicate rows",
    },
    {
        label: "Remove missing rows",
        instruction: "Remove rows with missing values",
    },
    {
        label: "Fill with mean",
        instruction: "Fill missing values in COLUMN with the mean",
    },
    {
        label: "Fill with median",
        instruction: "Fill missing values in COLUMN with the median",
    },
    {
        label: "Drop column",
        instruction: "Drop the COLUMN column",
    },
    {
        label: "Rename column",
        instruction: "Rename COLUMN to NEW_COLUMN",
    },
];


function CleaningAssistant({
    onClean,
    loading,
    disabled,
    error,
}) {
    const [instruction, setInstruction] = useState("");


    async function handleSubmit(event) {
        event.preventDefault();

        const cleanedInstruction = instruction.trim();

        if (!cleanedInstruction) {
            return;
        }

        await onClean(cleanedInstruction);
    }


    function handleActionClick(actionInstruction) {
        setInstruction(actionInstruction);
    }


    return (
        <section
            className="dashboard-card cleaning-assistant"
            id="cleaner"
        >

            <div className="section-title">
                <span className="section-icon">
                    ✦
                </span>

                <h2>AI Cleaning Assistant</h2>
            </div>


            <p className="assistant-description">
                Describe the cleaning task you want the AI to perform.
            </p>


            <form
                className="cleaning-form"
                onSubmit={handleSubmit}
            >
                <textarea
                    value={instruction}
                    onChange={(event) =>
                        setInstruction(event.target.value)
                    }
                    placeholder="e.g. Remove duplicate rows"
                    disabled={disabled || loading}
                    rows="4"
                />


                <div className="cleaning-form-actions">
                    <button
                        type="submit"
                        disabled={
                            disabled ||
                            loading ||
                            !instruction.trim()
                        }
                    >
                        {loading ? "Cleaning..." : "▷ Run"}
                    </button>
                </div>
            </form>


            <div className="available-actions">

                <span className="available-actions-label">
                    Available actions
                </span>

                <div className="action-list">

                    {AVAILABLE_ACTIONS.map((action) => (
                        <button
                            key={action.label}
                            type="button"
                            className="action-chip"
                            disabled={disabled || loading}
                            onClick={() =>
                                handleActionClick(
                                    action.instruction
                                )
                            }
                        >
                            {action.label}
                        </button>
                    ))}

                </div>

            </div>


            {error && (
                <div
                    className="cleaning-error"
                    role="alert"
                >
                    {error}
                </div>
            )}

        </section>
    );
}


export default CleaningAssistant;