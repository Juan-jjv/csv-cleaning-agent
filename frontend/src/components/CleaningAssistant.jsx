import { useState } from "react";


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
                Describe the cleaning task you want the AI
                to perform.
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
                        {loading ? "Cleaning..." : "▷  Run"}
                    </button>

                </div>

            </form>


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