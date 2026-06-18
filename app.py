### 1.Работа с API. Извлечение данных изи OpenAPI T-Invest.
import os
import requests
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

TOKEN = os.getenv('T_TOKEN')
URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

intervals_dict = {
    "1min": "CANDLE_INTERVAL_1_MIN",
    "5min": "CANDLE_INTERVAL_5_MIN",
    "15min": "CANDLE_INTERVAL_15_MIN",
    "hour": "CANDLE_INTERVAL_HOUR",
    "day": "CANDLE_INTERVAL_DAY"
}

figi = "BBG004730N88" # FIGI Сбербанк
interval = '15min'
from_dt = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
to_dt = datetime.now(timezone.utc).isoformat()

data = {
    "figi": figi,
    "from": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
    "to": datetime.now(timezone.utc).isoformat(),
    "interval": intervals_dict[interval]
}

logging.info(f"Запрос к API: figi={figi}, interval={interval}, from={from_dt}")

response = requests.post(url = URL, headers=headers, json=data)

if response.status_code == 200:
    # return response.json()
    df = pd.json_normalize(response.json()['candles'], sep='_')
    df.head()
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
    # return None
    print(None)

logging.info(f"Получено {len(df)} свечей из API")

### 2. Обработка DF данных.
df['open'] = df['open_units'].astype(float) + df['open_nano'] / 1000000000
df['close'] = df['close_units'].astype(float) + df['close_nano'] / 1000000000
df['high'] = df['high_units'].astype(float) + df['high_nano'] / 1000000000
df['low'] = df['low_units'].astype(float) + df['low_nano'] / 1000000000
df['interval'] = intervals_dict[interval]
df['figi'] = figi


ren_col = {
    'isComplete': 'is_complete',
    'candleSource': 'candle_source',
    'volumeBuy': 'volume_buy',
    'volumeSell': 'volume_sell'
}

df = df.rename(columns=ren_col)

### 3. Подключение к БД Postgres (Docker). Разово создаем витрину (если нужно).

from sqlalchemy import create_engine, text

conn = create_engine('postgresql://postgres:postgres@localhost:5051/postgres') # 5051 это бд под клиентом Airflow
cursor = conn.connect()

# Создаю витрину если нужно
sql = '''
    CREATE TABLE IF NOT EXISTS candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()


#создаем temp_candles с нужными типами данных
sql = '''
    DROP TABLE IF EXISTS temp_candles;
    CREATE TABLE IF NOT EXISTS temp_candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()

#загружаю данные в temp_candles
df.to_sql(
    'temp_candles', 
    conn, 
    if_exists='append', 
    index=False,
    method='multi'
)

logging.info(f"Загружено {len(df)} строк в temp_candles")

#делаю инкрементальную загрузку
sql = '''
    DELETE FROM candles
    WHERE (time, figi, interval) IN (
        SELECT time, figi, interval 
        FROM temp_candles
    );
    INSERT INTO candles
    SELECT * FROM temp_candles;
'''
cursor.execute(text(sql))
cursor.commit()
cursor.close()

logging.info("Инкрементальная загрузка завершена")

#Проверка на дубликаты
sql = '''
    select figi, interval, time, count(*) as cnt_rows
    FROM candles 
    GROUP BY figi, interval, time
    HAVING COUNT(*) > 1;
'''
df_test_db = pd.read_sql(sql, conn)

if df_test_db.empty:
    logging.info("Нет дубликатов")
else:
    logging.error("Есть дубликаты")
    logging.error(df_test_db.to_string())