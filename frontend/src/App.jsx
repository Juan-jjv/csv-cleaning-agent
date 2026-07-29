import { useState } from "react";

import {
    uploadCsv,
    cleanCsv,
    downloadCsv,
} from "./services/api";

import CleaningAssistant from "./components/CleaningAssistant";
import DownloadButton from "./components/DownloadButton";

import "./App.css";


function App() {
    const [sessionId, setSessionId] = useState(null);
    const [filename, setFilename] = useState("");
    const [stats, setStats] = useState(null);
    const [columnNames, setColumnNames] = useState([]);
    const [preview, setPreview] = useState([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [cleaning, setCleaning] = useState(false);
    const [cleaningResult, setCleaningResult] = useState(null);

    const [downloading, setDownloading] = useState(false);


    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setLoading(true);
        setError("");
        setCleaningResult(null);

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


    async function handleClean(instruction) {
        if (!sessionId) {
            return;
        }

        setCleaning(true);
        setError("");

        try {
            const data = await cleanCsv(
                sessionId,
                instruction,
            );

            setStats(data.stats);
            setColumnNames(data.column_names);
            setPreview(data.preview);

            setCleaningResult({
                command: data.command,
                confidence: data.confidence,
                summary: data.summary,
            });

        } catch (error) {
            setError(error.message);

        } finally {
            setCleaning(false);
        }
    }


    async function handleDownload() {
        if (!sessionId) {
            return;
        }

        setDownloading(true);
        setError("");

        try {
            const blob = await downloadCsv(sessionId);

            const url = window.URL.createObjectURL(blob);

            const link = document.createElement("a");

            link.href = url;

            link.download = filename
                ? `cleaned_${filename}`
                : "cleaned_data.csv";

            document.body.appendChild(link);

            link.click();

            link.remove();

            window.URL.revokeObjectURL(url);

        } catch (error) {
            setError(error.message);

        } finally {
            setDownloading(false);
        }
    }


    return (
        <div className="app">

            <header className="header">
                <div>
                    <h1>CSV Cleaning Agent</h1>
                    <p>Clean and transform your data with AI</p>
                </div>

                <div className="header-actions">

                    <label className="upload-button">
                        {loading ? "Uploading..." : "Upload CSV"}

                        <input
                            type="file"
                            accept=".csv"
                            onChange={handleUpload}
                            disabled={loading}
                            hidden
                        />
                    </label>

                    <DownloadButton
                        onDownload={handleDownload}
                        disabled={!sessionId}
                        loading={downloading}
                    />

                </div>
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


                        <CleaningAssistant
                            onClean={handleClean}
                            loading={cleaning}
                            disabled={!sessionId}
                            result={cleaningResult}
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