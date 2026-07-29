import StatCard from "./StatCard";


function StatsGrid({ stats }) {
    return (
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
    );
}


export default StatsGrid;