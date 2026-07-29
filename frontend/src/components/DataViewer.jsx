function DataViewer({
    columns,
    rows,
    page,
    totalPages,
    totalRows,
    loading,
    error,
    onPageChange,
    onClose,
}) {
    return (
        <div className="data-viewer-overlay">

            <div
                className="data-viewer"
                role="dialog"
                aria-modal="true"
                aria-label="Full dataset"
            >

                <div className="data-viewer-header">

                    <div>
                        <h2>Full Dataset</h2>

                        <p>
                            {totalRows.toLocaleString()} rows
                        </p>
                    </div>


                    <button
                        type="button"
                        className="viewer-close"
                        onClick={onClose}
                        aria-label="Close dataset viewer"
                    />

                </div>


                {error && (
                    <div
                        className="cleaning-error"
                        role="alert"
                    >
                        {error}
                    </div>
                )}


                {loading ? (
                    <div className="viewer-loading">
                        Loading dataset...
                    </div>
                ) : (
                    <div className="viewer-table-wrapper">

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
                )}


                <div className="viewer-footer">

                    <button
                        type="button"
                        className="pagination-button"
                        disabled={page <= 1 || loading}
                        onClick={() =>
                            onPageChange(page - 1)
                        }
                    >
                        <span>←</span>
                        Previous
                    </button>


                    <div className="page-indicator">

                        <span>Page</span>

                        <strong>
                            {page}
                        </strong>

                        <span>of</span>

                        <strong>
                            {totalPages}
                        </strong>

                    </div>


                    <button
                        type="button"
                        className="pagination-button"
                        disabled={
                            page >= totalPages ||
                            loading
                        }
                        onClick={() =>
                            onPageChange(page + 1)
                        }
                    >
                        Next
                        <span>→</span>
                    </button>

                </div>

            </div>

        </div>
    );
}


export default DataViewer;