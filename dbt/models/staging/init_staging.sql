create table if not exists staging.candles(
    datetime TIMESTAMPTZ NOT NULL,
    figi VARCHAR(255) NOT NULL,
    interval VARCHAR(255) NOT NULL,
    open DECIMAL(12,2),
    close DECIMAL(12,2),
    high DECIMAL(12,2),
    low DECIMAL(12,2),
    is_complete BOOLEAN,
    candle_source VARCHAR(255),
    volume BIGINT,
    volume_buy BIGINT,
    volume_sell BIGINT,
    source_job_id INTEGER,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
    )