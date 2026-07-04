CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE raw.extract_api_jobs IF NOT EXISTS (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,      -- например, 'MarketDataService/GetCandles'
    request_payload JSONB,               -- что отправляли (figi, from, to, interval)
    response_data JSONB,                -- что пришло от API (весь ответ)
    status_code INTEGER,                -- 200, 404, 500
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dim_calendar (
    date_id DATE PRIMARY KEY,
    year SMALLINT,
    month SMALLINT,
    day SMALLINT,
    quarter SMALLINT,
    week_number SMALLINT,
    day_of_week SMALLINT,           -- 1 = Monday, 7 = Sunday
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE,
    is_trading_day BOOLEAN DEFAULT TRUE,
    day_name VARCHAR(20),
    month_name VARCHAR(20),
    first_day_of_month DATE,
    last_day_of_month DATE,
    -- можно добавить любые другие поля по необходимости
    UNIQUE (date_id)
);

INSERT INTO dim_calendar (date_id, year, month, day, quarter, week_number, day_of_week, is_weekend, day_name, month_name, first_day_of_month, last_day_of_month)
SELECT
    d::DATE,
    EXTRACT(YEAR FROM d)::SMALLINT,
    EXTRACT(MONTH FROM d)::SMALLINT,
    EXTRACT(DAY FROM d)::SMALLINT,
    EXTRACT(QUARTER FROM d)::SMALLINT,
    EXTRACT(WEEK FROM d)::SMALLINT,
    EXTRACT(ISODOW FROM d)::SMALLINT,  -- ISO: 1 = Monday, 7 = Sunday
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6, 7) THEN TRUE ELSE FALSE END,
    TO_CHAR(d, 'Day') AS day_name,
    TO_CHAR(d, 'Month') AS month_name,
    DATE_TRUNC('month', d)::DATE,
    (DATE_TRUNC('month', d) + INTERVAL '1 month' - INTERVAL '1 day')::DATE
FROM generate_series('2025-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) AS d
ON CONFLICT (date_id) DO NOTHING;