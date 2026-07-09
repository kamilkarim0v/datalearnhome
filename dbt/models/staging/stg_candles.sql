WITH raw_data AS (
    SELECT
        jsonb_array_elements(response_data -> 'candles') AS candle,
        request_payload #>> '{figi}' AS figi,
        request_payload #>> '{interval}' AS interval,
        id AS source_job_id
    FROM raw.extract_api_jobs
    WHERE endpoint = 'MarketDataService/GetCandles'
      AND status_code = 200
)
SELECT
    (candle ->> 'time')::TIMESTAMPTZ AS datetime,
    figi,
    interval,
    ((candle -> 'open' ->> 'units')::DECIMAL + (candle -> 'open' ->> 'nano')::DECIMAL / 1e9) AS open,
    ((candle -> 'close' ->> 'units')::DECIMAL + (candle -> 'close' ->> 'nano')::DECIMAL / 1e9) AS close,
    ((candle -> 'high' ->> 'units')::DECIMAL + (candle -> 'high' ->> 'nano')::DECIMAL / 1e9) AS high,
    ((candle -> 'low' ->> 'units')::DECIMAL + (candle -> 'low' ->> 'nano')::DECIMAL / 1e9) AS low,
    (candle ->> 'isComplete')::BOOLEAN AS is_complete,
    candle ->> 'candleSource' AS candle_source,
    (candle ->> 'volume')::BIGINT AS volume,
    (candle ->> 'volumeBuy')::BIGINT AS volume_buy,
    (candle ->> 'volumeSell')::BIGINT AS volume_sell,
    source_job_id,
    CURRENT_TIMESTAMP AS loaded_at
FROM raw_data