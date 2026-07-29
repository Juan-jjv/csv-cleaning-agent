function DownloadButton({
    onDownload,
    disabled,
    loading,
}) {
    return (
        <button
            className="download-button"
            onClick={onDownload}
            disabled={disabled || loading}
        >
            {loading ? "Downloading..." : "Download CSV"}
        </button>
    );
}


export default DownloadButton;