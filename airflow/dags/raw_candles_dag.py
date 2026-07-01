from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Добавляем путь к корню проекта
sys.path.insert(0, '/opt/airflow')

from src_main.market_data import MarketDataClient
from src_main.db_manager import DatabaseManager 
from src_main.api_job_logger import ApiJobLogger
from datetime import timedelta, datetime, timezone

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
    'raw_candles_dag', # уникальное имя
    default_args=default_args,
    description='Запрос в T-Invest API и загрузка результатов в Postgres',
    schedule_interval='0 9 * * *', # каждый день в 9:00
    catchup=False, # не запускать пропущенные дни
    tags=['tinvest', 'etl'],
)

def init_db(dag):
    """Создаёт схему и таблицу, если их нет."""
    db = DatabaseManager()

    db_table_col = {
    'id': 'BIGSERIAL PRIMARY KEY',
    'endpoint': 'VARCHAR(255) NOT NULL',
    'request_payload': 'JSONB',        
    'response_data': 'JSONB', 
    'status_code': 'INTEGER', 
    'loaded_at': 'TIMESTAMPTZ DEFAULT NOW()'
    }

    db.create_schema(schema_name='raw')
    db.create_table(table_name='raw.extract_api_jobs', columns_type=db_table_col)

def extract_api_jobs(**context):
    """Извлекает данные из API и сохраняет их в XCom."""

    client = MarketDataClient()

    # пока зафиксим жестко
    figi = "BBG004730N88"
    interval = "15min"
    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=1)
    (response, status_code), endpoint, payload = client.get_candles(figi, from_dt, to_dt, interval)

    # Сохраняем в XCom для следующей задачи
    context['ti'].xcom_push(key='response', value=response)
    context['ti'].xcom_push(key='endpoint', value=endpoint)
    context['ti'].xcom_push(key='payload', value=payload)
    context['ti'].xcom_push(key='status_code', value=status_code)

def load_data(**context):
    """Забирает данные из XCom и логирует в БД."""
    ti = context['ti']
    response = ti.xcom_pull(task_ids='extract_api_jobs', key='response')
    endpoint = ti.xcom_pull(task_ids='extract_api_jobs', key='endpoint')
    payload = ti.xcom_pull(task_ids='extract_api_jobs', key='payload')
    status_code = ti.xcom_pull(task_ids='extract_api_jobs', key='status_code')

    db = DatabaseManager()
    logger = ApiJobLogger(db)
    logger.save_job(
        endpoint=endpoint,
        request_payload=payload,
        response_data=response,
        status_code=status_code
    )

task_init_db = PythonOperator(
    task_id='init_db',
    python_callable=init_db,
    dag=dag,
)

task_extract_data = PythonOperator(
    task_id='extract_api_jobs',
    python_callable=extract_api_jobs,
    provide_context=True,  # чтобы был доступ к context['ti']
    dag=dag,
)

task_load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

task_init_db >> task_extract_data >> task_load_data