function DatasetPreview({
    columns,
    rows,
}) {
    if (rows.length === 0) {
        return (
            <section className="preview-section">
                <h2>Dataset Preview</h2>
                <p>No rows to preview.</p>
            </section>
        );
    }

    return (
        <section className="preview-section">

            <h2>Dataset Preview</h2>

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

        </section>
    );
}


export default DatasetPreview;