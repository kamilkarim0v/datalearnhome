from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к корню проекта
sys.path.insert(0, '/opt/airflow')

# Импортируем ETL-класс
from src.etl_pipeline import CandlesETL

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
    'candles_etl_daily', # уникальное имя
    default_args=default_args,
    description='Загрузка свечей из T-Invest API в PostgreSQL',
    schedule_interval='0 9 * * *', # каждый день в 9:00
    catchup=False, # не запускать пропущенные дни
    tags=['tinvest', 'etl'],
)

# Функция, которую будет выполнять таск
def run_etl(**context):
    # Параметры можно вынести в Variables или оставить жёстко
    figi = 'BBG004730N88'
    interval = '15min'
    days_back = 1
    etl = CandlesETL(figi, interval, days_back)
    etl.run()

# Создаём таск
task_load_candles = PythonOperator(
    task_id='load_candles',
    python_callable=run_etl,
    dag=dag,
)

# Если несколько тасков, определяем порядок, но у нас один
task_load_candles