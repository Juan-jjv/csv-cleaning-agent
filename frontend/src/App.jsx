import { useState } from "react";

import {
    uploadCsv,
    cleanCsv,
    downloadCsv,
} from "./services/api";

import Header from "./components/Header";
import StatsGrid from "./components/StatsGrid";
import DatasetPreview from "./components/DatasetPreview";
import CleaningAssistant from "./components/CleaningAssistant";

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
    const [cleaningError, setCleaningError] = useState("");

    const [downloading, setDownloading] = useState(false);


    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setLoading(true);
        setError("");

        setCleaningResult(null);
        setCleaningError("");

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
        setCleaningError("");

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
            setCleaningResult(null);
            setCleaningError(error.message);

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

            <Header
                onUpload={handleUpload}
                uploading={loading}
                onDownload={handleDownload}
                downloading={downloading}
                downloadDisabled={!sessionId}
            />


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

                    <h2>
                        Upload a CSV to get started
                    </h2>

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


                    <StatsGrid
                        stats={stats}
                    />


                    <DatasetPreview
                        columns={columnNames}
                        rows={preview}
                    />


                    <CleaningAssistant
                        onClean={handleClean}
                        loading={cleaning}
                        disabled={!sessionId}
                        result={cleaningResult}
                        error={cleaningError}
                    />

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


export default App;