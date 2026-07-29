import UploadButton from "./UploadButton";
import DownloadButton from "./DownloadButton";


function Header({
    onUpload,
    uploading,
    onDownload,
    downloading,
    downloadDisabled,
}) {
    return (
        <header className="page-header">

            <h1>CSV Cleaning Agent</h1>


            <div className="header-actions">

                <UploadButton
                    onUpload={onUpload}
                    loading={uploading}
                />

                <DownloadButton
                    onDownload={onDownload}
                    disabled={downloadDisabled}
                    loading={downloading}
                />

            </div>

        </header>
    );
}


export default Header;