import { useState } from "react";


function CleaningAssistant({
    onClean,
    loading,
    disabled,
    result,
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


    return (
        <section className="cleaning-assistant">
            <div className="cleaning-assistant-header">
                <div>
                    <h2>AI Cleaning Assistant</h2>
                    <p>
                        Describe how you want to clean your dataset.
                    </p>
                </div>
            </div>

            <form
                className="cleaning-form"
                onSubmit={handleSubmit}
            >
                <input
                    type="text"
                    value={instruction}
                    onChange={(event) =>
                        setInstruction(event.target.value)
                    }
                    placeholder="e.g. Fill missing salary values with the mean"
                    disabled={disabled || loading}
                />

                <button
                    type="submit"
                    disabled={
                        disabled ||
                        loading ||
                        !instruction.trim()
                    }
                >
                    {loading ? "Cleaning..." : "Run"}
                </button>
            </form>

            {result && (
                <div className="cleaning-result">
                    <p>
                        <strong>Action:</strong>{" "}
                        {result.command.action}
                    </p>

                    <p>
                        <strong>Confidence:</strong>{" "}
                        {(result.confidence * 100).toFixed(1)}%
                    </p>
                </div>
            )}
        </section>
    );
}


export default CleaningAssistant;