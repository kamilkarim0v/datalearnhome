from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Добавляем путь к корню проекта
sys.path.insert(0, '/opt/airflow')

# from src_main.market_data import MarketDataService
from src_main.db_manager import DatabaseManager 

# Параметры по умолчанию для DAG
default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Определяем DAG
dag = DAG(
    'staging_candles_dag', # уникальное имя
    default_args=default_args,
    description='Запрос в T-Invest API и загрузка результатов в Postgres',
    schedule_interval='0 9 * * *', # каждый день в 9:00
    catchup=False, # не запускать пропущенные дни
    tags=['staging', 'etl'],
)

def init_db():
    """Создаёт схему и таблицу, если их нет."""
    db = DatabaseManager()

    db_table_col = {
    'datetime': 'TIMESTAMPTZ NOT NULL',
    'figi': 'VARCHAR(255) NOT NULL',
    'interval': 'VARCHAR(255) NOT NULL',
    'open': 'DECIMAL(12,2)',
    'close': 'DECIMAL(12,2)',
    'high': 'DECIMAL(12,2)',
    'low': 'DECIMAL(12,2)',
    'is_complete': 'BOOLEAN',
    'candle_source': 'VARCHAR(255)',
    'volume': 'BIGINT',
    'volume_buy': 'BIGINT',
    'volume_sell': 'BIGINT',
    'source_job_id': 'INTEGER',
    'loaded_at': 'TIMESTAMPTZ DEFAULT NOW()'
    }

    primary_key = ['datetime', 'figi', 'interval']

    db.create_schema(schema_name='staging')
    db.create_table(table_name='staging.candles', columns_type=db_table_col, primary_key=primary_key)

