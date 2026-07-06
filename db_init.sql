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

-- 1. Создаём таблицу (если её нет) с увеличенной точностью
CREATE TABLE IF NOT EXISTS raw.candles_interval_limits (
    interval_full VARCHAR(50) PRIMARY KEY,
    interval_short VARCHAR(20) NOT NULL,
    max_limit INTEGER NOT NULL,
    candles_per_day DECIMAL(12,6) NOT NULL,   -- было DECIMAL(10,6) → теперь 12,6
    max_days_calc INTEGER GENERATED ALWAYS AS (FLOOR(max_limit / candles_per_day)) STORED,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Заполняем таблицу
INSERT INTO raw.candles_interval_limits (interval_full, interval_short, max_limit, candles_per_day, description)
VALUES
('CANDLE_INTERVAL_1_MIN',    '1min',  2400, 1440,    'От 1 минуты до 1 дня'),
('CANDLE_INTERVAL_2_MIN',    '2min',  1200, 720,     'От 2 минут до 1 дня'),
('CANDLE_INTERVAL_3_MIN',    '3min',  750,  480,     'От 3 минут до 1 дня'),
('CANDLE_INTERVAL_5_MIN',    '5min',  2400, 288,     'От 5 минут до недели'),
('CANDLE_INTERVAL_10_MIN',   '10min', 1200, 144,     'От 10 минут до недели'),
('CANDLE_INTERVAL_15_MIN',   '15min', 2400, 96,      'От 15 минут до 3 недель'),
('CANDLE_INTERVAL_30_MIN',   '30min', 1200, 48,      'От 30 минут до 3 недель'),
('CANDLE_INTERVAL_HOUR',     'hour',  2400, 24,      'От 1 часа до 3 месяцев'),
('CANDLE_INTERVAL_2_HOUR',   '2hour', 2400, 12,      'От 2 часов до 3 месяцев'),
('CANDLE_INTERVAL_4_HOUR',   '4hour', 700,  6,       'От 4 часов до 3 месяцев'),
('CANDLE_INTERVAL_DAY',      'day',   2400, 1,       'От 1 дня до 6 лет'),
('CANDLE_INTERVAL_WEEK',     'week',  300,  0.142857,'От 1 недели до 5 лет'),  -- 1/7 ≈ 0.142857
('CANDLE_INTERVAL_MONTH',    'month', 120,  0.03333, 'От 1 месяца до 10 лет'), -- 1/30 ≈ 0.03333
('CANDLE_INTERVAL_5_SEC',    '5sec',  2500, 17280,   'От 5 секунд до 200 минут'),  -- 17280 свечей/день
('CANDLE_INTERVAL_10_SEC',   '10sec', 1250, 8640,    'От 10 секунд до 200 минут'),
('CANDLE_INTERVAL_30_SEC',   '30sec', 2500, 2880,    'От 30 секунд до 20 часов')
ON CONFLICT (interval_full) DO NOTHING;

-- 3. Комментарии (опционально)
COMMENT ON TABLE raw.candles_interval_limits IS 'Лимиты API T-Invest для разных интервалов свечей';
COMMENT ON COLUMN raw.candles_interval_limits.max_days_calc IS 'Максимальное количество дней, которое можно запросить за один вызов, исходя из лимита свечей';