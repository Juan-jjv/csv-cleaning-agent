import { useState } from "react";

import {
    uploadCsv,
    cleanCsv,
    downloadCsv,
    getDatasetPage,
} from "./services/api";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import StatsGrid from "./components/StatsGrid";
import DatasetPreview from "./components/DatasetPreview";
import CleaningAssistant from "./components/CleaningAssistant";
import LatestResult from "./components/LatestResult";
import DataViewer from "./components/DataViewer";

import "./App.css";


const DATA_PAGE_SIZE = 50;


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

    const [viewerOpen, setViewerOpen] = useState(false);
    const [viewerColumns, setViewerColumns] = useState([]);
    const [viewerRows, setViewerRows] = useState([]);
    const [viewerPage, setViewerPage] = useState(1);
    const [viewerTotalPages, setViewerTotalPages] = useState(1);
    const [viewerTotalRows, setViewerTotalRows] = useState(0);
    const [viewerLoading, setViewerLoading] = useState(false);
    const [viewerError, setViewerError] = useState("");


    async function handleUpload(event) {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        setLoading(true);
        setError("");
        setCleaningResult(null);
        setCleaningError("");
        setViewerOpen(false);

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

            setViewerOpen(false);

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


    async function loadDatasetPage(page) {
        if (!sessionId) {
            return;
        }

        setViewerLoading(true);
        setViewerError("");

        try {
            const data = await getDatasetPage(
                sessionId,
                page,
                DATA_PAGE_SIZE,
            );

            setViewerColumns(data.columns);
            setViewerRows(data.rows);
            setViewerPage(data.page);
            setViewerTotalPages(data.total_pages);
            setViewerTotalRows(data.total_rows);

        } catch (error) {
            setViewerError(error.message);

        } finally {
            setViewerLoading(false);
        }
    }


    async function handleViewAll() {
        if (!sessionId) {
            return;
        }

        setViewerOpen(true);

        await loadDatasetPage(1);
    }


    async function handleViewerPageChange(page) {
        await loadDatasetPage(page);
    }


    function handleCloseViewer() {
        setViewerOpen(false);
    }


    return (
        <div className="app-shell">

            <Sidebar hasDataset={Boolean(sessionId)} />

            <main
                className="main-content"
                id="home"
            >

                <Header
                    onUpload={handleUpload}
                    uploading={loading}
                    onDownload={handleDownload}
                    downloading={downloading}
                    downloadDisabled={!sessionId}
                />


                {error && (
                    <div className="error">
                        {error}
                    </div>
                )}


                {!stats && !loading && (
                    <div className="empty-state">

                        <h2>
                            Upload a CSV to get started
                        </h2>

                        <p>
                            Your dataset dashboard will
                            appear here.
                        </p>

                    </div>
                )}


                {loading && (
                    <div className="loading-message">
                        Uploading CSV...
                    </div>
                )}


                {stats && (
                    <>

                        <StatsGrid
                            stats={stats}
                        />


                        <DatasetPreview
                            columns={columnNames}
                            rows={preview}
                            totalRows={stats.rows}
                            onViewAll={handleViewAll}
                        />


                        <div className="bottom-dashboard-grid">

                            <CleaningAssistant
                                onClean={handleClean}
                                loading={cleaning}
                                disabled={!sessionId}
                                error={cleaningError}
                            />


                            <LatestResult
                                result={cleaningResult}
                            />

                        </div>

                    </>
                )}

            </main>


            {viewerOpen && (
                <DataViewer
                    columns={viewerColumns}
                    rows={viewerRows}
                    page={viewerPage}
                    totalPages={viewerTotalPages}
                    totalRows={viewerTotalRows}
                    loading={viewerLoading}
                    error={viewerError}
                    onPageChange={handleViewerPageChange}
                    onClose={handleCloseViewer}
                />
            )}

        </div>
    );
}


export default App;