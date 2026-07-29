function Sidebar({ hasDataset }) {
    return (
        <aside className="sidebar">

            <div className="sidebar-brand">
                <div className="brand-icon">
                    AI
                </div>

                <div>
                    <strong>CSV Cleaning</strong>
                    <span>Agent</span>
                </div>
            </div>


            <nav className="sidebar-nav">

                <a
                    href="#home"
                    className="sidebar-link active"
                >
                    <span className="sidebar-link-icon">
                        ⌂
                    </span>

                    Home
                </a>


                {hasDataset && (
                    <>
                        <a
                            href="#dataset"
                            className="sidebar-link"
                        >
                            <span className="sidebar-link-icon">
                                ▤
                            </span>

                            Dataset
                        </a>

                        <a
                            href="#cleaner"
                            className="sidebar-link"
                        >
                            <span className="sidebar-link-icon">
                                ✦
                            </span>

                            AI Cleaner
                        </a>
                    </>
                )}

            </nav>

        </aside>
    );
}


export default Sidebar;