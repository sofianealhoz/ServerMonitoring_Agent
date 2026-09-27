-- Table read and written by /history.
-- Apply once: psql "postgresql://postgreuser:postgrepswd@localhost:5432/dbname_monitoring" -f sql/schema.sql
CREATE TABLE IF NOT EXISTS metric_samples (
    id          SERIAL PRIMARY KEY,
    cpu_usage   NUMERIC(5, 2) CHECK (cpu_usage BETWEEN 0 AND 100),
    ram_usage   NUMERIC(5, 2) CHECK (ram_usage BETWEEN 0 AND 100),
    disk_usage  NUMERIC(5, 2) CHECK (disk_usage BETWEEN 0 AND 100)
);

-- Accounts allowed to call the API. Passwords are stored HASHED (bcrypt), never in clear.
-- Create one with: python3 src/create_user.py <username> <reader|admin>
CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    username         TEXT UNIQUE NOT NULL,
    hashed_password  TEXT NOT NULL,
    role             TEXT NOT NULL CHECK (role IN ('reader', 'admin')),
    disabled         BOOLEAN NOT NULL DEFAULT FALSE
);
