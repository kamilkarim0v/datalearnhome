CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE raw.extract_api_jobs IF NOT EXISTS (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,      -- например, 'MarketDataService/GetCandles'
    request_payload JSONB,               -- что отправляли (figi, from, to, interval)
    response_data JSONB,                -- что пришло от API (весь ответ)
    status_code INTEGER,                -- 200, 404, 500
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);