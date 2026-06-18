from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'tinvest_candles_daily',
    default_args=default_args,
    schedule_interval='0 8 * * *',  # каждый день в 8 утра
    catchup=False,
)

def load_candles():
    # сюда вставить код из app.py
    pass

task = PythonOperator(
    task_id='load_candles_task',
    python_callable=load_candles,
    dag=dag,
)