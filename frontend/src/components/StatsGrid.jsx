import StatCard from "./StatCard";


function StatsGrid({ stats }) {
    return (
        <section className="stats-grid">

            <StatCard
                label="Rows"
                value={stats.rows}
                icon="▦"
                tone="purple"
            />

            <StatCard
                label="Columns"
                value={stats.columns}
                icon="▤"
                tone="green"
            />

            <StatCard
                label="Missing Values"
                value={stats.missing_values}
                icon="!"
                tone="orange"
            />

            <StatCard
                label="Duplicate Rows"
                value={stats.duplicate_rows}
                icon="▣"
                tone="red"
            />

        </section>
    );
}


export default StatsGrid;