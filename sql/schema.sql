-- Table read and written by /history.
-- Apply once: psql "postgresql://postgreuser:postgrepswd@localhost:5432/dbname_monitoring" -f sql/schema.sql
CREATE TABLE IF NOT EXISTS metric_samples (
    id          SERIAL PRIMARY KEY,
    cpu_usage   NUMERIC(5, 2) CHECK (cpu_usage BETWEEN 0 AND 100),
    ram_usage   NUMERIC(5, 2) CHECK (ram_usage BETWEEN 0 AND 100),
    disk_usage  NUMERIC(5, 2) CHECK (disk_usage BETWEEN 0 AND 100)
);
