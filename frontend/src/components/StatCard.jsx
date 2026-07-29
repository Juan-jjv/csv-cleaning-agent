function StatCard({
    label,
    value,
    icon,
    tone,
}) {
    return (
        <div className="stat-card">

            <div
                className={`stat-icon stat-icon-${tone}`}
            >
                {icon}
            </div>

            <div className="stat-content">
                <span>{label}</span>

                <strong>
                    {value.toLocaleString()}
                </strong>
            </div>

        </div>
    );
}


export default StatCard;