DROP TABLE IF EXISTS metric_samples CASCADE;
DROP TABLE IF EXISTS network_samples CASCADE;
DROP TABLE IF EXISTS process_samples CASCADE;
DROP TABLE IF EXISTS log_stats CASCADE;
DROP TABLE IF EXISTS user_info CASCADE;
DROP TABLE IF EXISTS ram_samples CASCADE;
DROP TABLE IF EXISTS hdd_samples CASCADE;

CREATE TABLE IF NOT EXISTS metric_samples (
    cpu_usage       NUMERIC(6,3),   -- %
    ram_usage       NUMERIC(6,3),   -- %
    disk_usage      NUMERIC(6,3)    -- %
);

-- Snapshot RAM détaillé (src/domain/schemas/ram.py)
CREATE TABLE IF NOT EXISTS ram_samples (
    id              BIGSERIAL PRIMARY KEY,
    total_gb        NUMERIC(12,4),
    available_gb    NUMERIC(12,4),
    used_gb         NUMERIC(12,4),
    percent         NUMERIC(6,3),
    frequency_mhz   NUMERIC(10,3)
);

-- Snapshot HDD (src/domain/schemas/hdd.py)
CREATE TABLE IF NOT EXISTS hdd_samples (
    id              BIGSERIAL PRIMARY KEY,
    total_gb        NUMERIC(15,4),
    used_gb         NUMERIC(15,4),
    free_gb         NUMERIC(15,4),
    percent         NUMERIC(6,3)
);

-- Réseau par interface (src/domain/schemas/network.py)
CREATE TABLE IF NOT EXISTS network_samples (
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    bytes_sent      BIGINT,
    bytes_recv      BIGINT,
    packets_sent    BIGINT,
    packets_recv    BIGINT,
    errin           BIGINT,
    errout          BIGINT,
    dropin          BIGINT,
    dropout         BIGINT
);

-- Top processus (src/domain/schemas/process.py)
CREATE TABLE IF NOT EXISTS process_samples (
    id              BIGSERIAL PRIMARY KEY,
    pid             INTEGER,
    name            TEXT,
    rss_mb          NUMERIC(12,4),
    cpu_percent     NUMERIC(6,3)
);

-- Logs Apache (src/domain/schemas/log.py)
CREATE TABLE IF NOT EXISTS log_stats (
    id                  BIGSERIAL PRIMARY KEY,
    unique_users        INTEGER,
    nb_error404         INTEGER,
    last_5_error_logs   TEXT[]  -- correspond à List[str]
);

-- Informations utilisateur (src/domain/schemas/user.py)
CREATE TABLE IF NOT EXISTS user_info (
    id              BIGSERIAL PRIMARY KEY,
    nickname        TEXT,
    hostname        TEXT,
    ip              TEXT
);