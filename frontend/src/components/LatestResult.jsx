import ChangeSummary from "./ChangeSummary";


function LatestResult({ result }) {
    return (
        <section className="dashboard-card latest-result">

            <div className="section-title">
                <span className="section-icon">
                    ✓
                </span>

                <h2>Latest Result</h2>
            </div>


            {!result ? (
                <div className="latest-result-empty">
                    <p>No cleaning operation yet.</p>

                    <span>
                        Run an AI cleaning instruction to see
                        the result here.
                    </span>
                </div>
            ) : (
                <>

                    <ChangeSummary
                        command={result.command}
                        summary={result.summary}
                    />


                    <div className="result-metadata">

                        <div>
                            <span>Action</span>

                            <strong>
                                {result.command.action
                                    .replaceAll("_", " ")}
                            </strong>
                        </div>


                        <div>
                            <span>Confidence</span>

                            <strong>
                                {(result.confidence * 100)
                                    .toFixed(1)}%
                            </strong>
                        </div>

                    </div>

                </>
            )}

        </section>
    );
}


export default LatestResult;