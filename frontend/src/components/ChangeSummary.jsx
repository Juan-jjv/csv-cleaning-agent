function ChangeSummary({ command, summary }) {
    if (!command || !summary) {
        return null;
    }

    const action = command.action;

    if (action === "remove_duplicates") {
        return (
            <div className="change-summary">
                <strong>
                    Removed {summary.rows_removed} duplicate row(s)
                </strong>

                <span>
                    Rows: {summary.rows_before} → {summary.rows_after}
                </span>
            </div>
        );
    }

    if (action === "remove_missing_rows") {
        return (
            <div className="change-summary">
                <strong>
                    Removed {summary.rows_removed} row(s) with missing values
                </strong>

                <span>
                    Rows: {summary.rows_before} → {summary.rows_after}
                </span>
            </div>
        );
    }

    if (
        action === "fill_missing_with_mean" ||
        action === "fill_missing_with_median"
    ) {
        return (
            <div className="change-summary">
                <strong>
                    Filled {summary.values_filled} missing value(s) in{" "}
                    {summary.column}
                </strong>

                <span>
                    Missing values: {summary.missing_before} →{" "}
                    {summary.missing_after}
                </span>
            </div>
        );
    }

    if (action === "drop_column") {
        return (
            <div className="change-summary">
                <strong>
                    Removed column: {summary.column_removed}
                </strong>

                <span>
                    Columns: {summary.columns_before} →{" "}
                    {summary.columns_after}
                </span>
            </div>
        );
    }

    if (action === "rename_column") {
        return (
            <div className="change-summary">
                <strong>
                    Renamed {summary.old_name} → {summary.new_name}
                </strong>
            </div>
        );
    }

    return null;
}


export default ChangeSummary;