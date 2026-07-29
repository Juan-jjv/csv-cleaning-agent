function UploadButton({
    onUpload,
    loading,
}) {
    return (
        <label className="upload-button">
            {loading ? "Uploading..." : "Upload CSV"}

            <input
                type="file"
                accept=".csv"
                onChange={onUpload}
                disabled={loading}
                hidden
            />
        </label>
    );
}


export default UploadButton;