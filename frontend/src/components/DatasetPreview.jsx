function DatasetPreview({
    columns,
    rows,
    totalRows,
    onViewAll,
}) {
    return (
        <section
            className="dashboard-card preview-section"
            id="dataset"
        >

            <h2>Dataset Preview</h2>


            {rows.length === 0 ? (
                <p className="empty-table-message">
                    No rows to preview.
                </p>
            ) : (
                <>
                    <div className="table-wrapper">

                        <table>
                            <thead>
                                <tr>
                                    {columns.map((column) => (
                                        <th key={column}>
                                            {column}
                                        </th>
                                    ))}
                                </tr>
                            </thead>

                            <tbody>
                                {rows.map((row, rowIndex) => (
                                    <tr key={rowIndex}>

                                        {columns.map((column) => (
                                            <td key={column}>
                                                {row[column] ?? "—"}
                                            </td>
                                        ))}

                                    </tr>
                                ))}
                            </tbody>
                        </table>

                    </div>


                    <div className="preview-footer">

                        <span>
                            Showing first {rows.length} of{" "}
                            {totalRows.toLocaleString()} rows
                        </span>


                        <button
                            type="button"
                            className="view-all-button"
                            onClick={onViewAll}
                        >
                            View all data
                            <span>→</span>
                        </button>

                    </div>
                </>
            )}

        </section>
    );
}


export default DatasetPreview;