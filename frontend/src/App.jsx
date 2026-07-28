import { useState } from "react";

import { uploadCsv } from "./services/api";

import "./App.css";


function App() {
    const [sessionId, setSessionId] = useState(null);
    const [filename, setFilename] = useState("");
    const [stats, setStats] = useState(null);
    const [columnNames, setColumnNames] = useState([]);
    const [preview, setPreview] = useState([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const data = await uploadCsv(file);

            setSessionId(data.session_id);
            setFilename(data.filename);
            setStats(data.stats);
            setColumnNames(data.column_names);
            setPreview(data.preview);

        } catch (error) {
            setError(error.message);

        } finally {
            setLoading(false);
        }
    }


    return (
        <div className="app">
            <header className="header">
                <div>
                    <h1>CSV Cleaning Agent</h1>
                    <p>Clean and transform your data with AI</p>
                </div>

                <label className="upload-button">
                    Upload CSV

                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleUpload}
                        hidden
                    />
                </label>
            </header>

            {loading && (
                <p>Uploading CSV...</p>
            )}

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

            {!stats && !loading && (
                <div className="empty-state">
                    <h2>Upload a CSV to get started</h2>
                    <p>
                        Your dataset information will appear here.
                    </p>
                </div>
            )}

            {stats && (
                <>
                    <section className="file-info">
                        <strong>{filename}</strong>
                    </section>

                    <section className="stats-grid">
                        <StatCard
                            label="Rows"
                            value={stats.rows}
                        />

                        <StatCard
                            label="Columns"
                            value={stats.columns}
                        />

                        <StatCard
                            label="Missing Values"
                            value={stats.missing_values}
                        />

                        <StatCard
                            label="Duplicate Rows"
                            value={stats.duplicate_rows}
                        />
                    </section>

                    <section className="preview-section">
                        <h2>Dataset Preview</h2>

                        <DatasetTable
                            columns={columnNames}
                            rows={preview}
                        />
                    </section>
                </>
            )}

            {sessionId && (
                <p className="session-debug">
                    Session: {sessionId}
                </p>
            )}
        </div>
    );
}


function StatCard({ label, value }) {
    return (
        <div className="stat-card">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
    );
}


function DatasetTable({ columns, rows }) {
    if (rows.length === 0) {
        return <p>No rows to preview.</p>;
    }

    return (
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
    );
}


export default App;