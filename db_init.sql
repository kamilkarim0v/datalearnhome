-- тут постараюсь описать логику что я хочу:
-- 1. Создать витрину с запросами к API

CREATE TABLE raw.extract_api_jobs (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,      -- например, 'MarketDataService/GetCandles'
    request_payload JSONB,               -- что отправляли (figi, from, to, interval)
    response_data JSONB,                -- что пришло от API (весь ответ)
    status_code INTEGER,                -- 200, 404, 500
    loaded_at TIMESTAMPTZ DEFAULT NOW(),
    figi VARCHAR(50),                   -- для быстрой фильтрации (если есть)
    interval VARCHAR(20),               -- для быстрой фильтрации (если есть)
    from_dt TIMESTAMPTZ,                -- для быстрой фильтрации
    to_dt TIMESTAMPTZ                   -- для быстрой фильтрации
);