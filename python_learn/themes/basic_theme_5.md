## Уровень 5: Оркестрация — Airflow и production пайплайны (недели 15–17)

---

### Шаг 1. Airflow — основы (3 дня)

#### 1.1 Что такое Airflow для DE

**Airflow — это не ETL-инструмент, а оркестратор.** Он не обрабатывает данные, а **запускает** ваши Python-скрипты в нужном порядке.

```python
# Базовый DAG (Directed Acyclic Graph)
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'de_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True
}

dag = DAG(
    'daily_etl',
    default_args=default_args,
    description='Ежедневная загрузка заказов',
    schedule='0 2 * * *',  # каждый день в 2:00
    start_date=datetime(2024, 1, 1),
    catchup=False,  # не выполнять пропущенные дни
    tags=['etl', 'orders']
)

def extract():
    # ваш код extract
    pass

def transform():
    # ваш код transform
    pass

def load():
    # ваш код load
    pass

# Задачи
task_extract = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
task_transform = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
task_load = PythonOperator(task_id='load', python_callable=load, dag=dag)

# Порядок выполнения
task_extract >> task_transform >> task_load
```

#### 1.2 Передача данных между задачами (XCom)

```python
from airflow.operators.python import PythonOperator

def extract(ti):
    df = pd.read_csv('data.csv')
    row_count = len(df)
    ti.xcom_push(key='row_count', value=row_count)  # сохраняем
    return df.to_dict()  # или через return

def transform(ti):
    row_count = ti.xcom_pull(key='row_count', task_ids='extract')
    print(f"Обрабатываем {row_count} строк")
    # ...
```

**Важно:** XCom не для больших данных. Для передачи DataFrame используйте S3/хранилище.

#### 1.3 Правильный паттерн (задачи через файлы)

```python
def extract(ti):
    df = pd.read_csv('source.csv')
    df.to_parquet('/tmp/extracted.parquet')
    ti.xcom_push(key='file_path', value='/tmp/extracted.parquet')

def transform(ti):
    file_path = ti.xcom_pull(key='file_path', task_ids='extract')
    df = pd.read_parquet(file_path)
    df_transformed = df.groupby('region').sum()
    df_transformed.to_parquet('/tmp/transformed.parquet')

def load(ti):
    file_path = ti.xcom_pull(key='file_path', task_ids='transform')
    df = pd.read_parquet(file_path)
    df.to_sql('target', engine, if_exists='append')
```

---

### Шаг 2. Practical operators (2 дня)

#### 2.1 SQLOperator — выполнить SQL в БД

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

sql_task = PostgresOperator(
    task_id='create_staging',
    postgres_conn_id='warehouse_conn',  # настраивается в UI
    sql="""
        CREATE TABLE IF NOT EXISTS staging_orders AS
        SELECT * FROM source_orders WHERE date > '2024-01-01';
    """,
    dag=dag
)
```

#### 2.2 BashOperator — запустить shell-скрипт

```python
from airflow.operators.bash import BashOperator

bash_task = BashOperator(
    task_id='run_etl_script',
    bash_command='python /opt/airflow/dags/scripts/etl.py --date {{ ds }}',
    dag=dag
)
```

#### 2.3 BranchOperator — условное ветвление

```python
from airflow.operators.python import BranchPythonOperator

def check_data(**context):
    df = pd.read_parquet('/tmp/data.parquet')
    if len(df) == 0:
        return 'skip_load'
    return 'load'

branch = BranchPythonOperator(
    task_id='branch',
    python_callable=check_data,
    dag=dag
)

branch >> [load_task, skip_load_task]
```

#### 2.4 Sensors — ждать внешний файл/условие

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id='wait_for_file',
    filepath='/incoming/orders.csv',
    poke_interval=30,  # проверять каждые 30 секунд
    timeout=3600,      # ждать максимум час
    dag=dag
)
```

---

### Шаг 3. Полноценный production ETL (3 дня)

#### 3.1 Структура DAG-файла

```python
# dag_daily_orders.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import logging
import pandas as pd
from sqlalchemy import create_engine

# Конфигурация
CONN_STRING = "postgresql://etl:pass@warehouse:5432/dwh"

default_args = {
    'owner': 'de_team',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email': ['alerts@company.com'],
    'email_on_failure': True,
}

dag = DAG(
    'daily_orders_etl',
    default_args=default_args,
    description='Загрузка заказов из CSV в DWH',
    schedule='30 1 * * *',  # в 01:30 каждый день
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,  # только один запуск одновременно
    tags=['orders', 'daily'],
)

def extract(**context):
    """Чтение CSV файлов за вчерашний день"""
    execution_date = context['ds']  # дата запуска DAG
    file_path = f"/data/incoming/orders_{execution_date}.csv"
    
    logging.info(f"Читаем файл: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")
    
    df = pd.read_csv(file_path)
    logging.info(f"Прочитано {len(df)} строк")
    
    # Сохраняем во временную папку
    staging_path = f"/tmp/orders_{execution_date}.parquet"
    df.to_parquet(staging_path, index=False)
    
    context['ti'].xcom_push(key='staging_path', value=staging_path)
    context['ti'].xcom_push(key='row_count', value=len(df))

def validate(**context):
    """Проверки качества"""
    staging_path = context['ti'].xcom_pull(key='staging_path', task_ids='extract')
    df = pd.read_parquet(staging_path)
    
    # Проверки
    if len(df) == 0:
        raise ValueError("Нет данных")
    
    if df['amount'].min() < 0:
        logging.error(f"Отрицательные суммы: {df[df['amount'] < 0]['amount'].tolist()[:5]}")
        raise ValueError("Найдены отрицательные суммы")
    
    if df['user_id'].isna().sum() > 0:
        raise ValueError("Есть строки без user_id")
    
    logging.info("Валидация пройдена")
    context['ti'].xcom_push(key='validated_path', value=staging_path)

def transform(**context):
    """Агрегация данных"""
    staging_path = context['ti'].xcom_pull(key='validated_path', task_ids='validate')
    df = pd.read_parquet(staging_path)
    
    # Агрегация
    result = df.groupby(['user_id', 'product_category']).agg({
        'amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    output_path = "/tmp/aggregated.parquet"
    result.to_parquet(output_path, index=False)
    
    context['ti'].xcom_push(key='aggregated_path', value=output_path)
    context['ti'].xcom_push(key='result_rows', value=len(result))

def load(**context):
    """Загрузка в PostgreSQL"""
    agg_path = context['ti'].xcom_pull(key='aggregated_path', task_ids='transform')
    df = pd.read_parquet(agg_path)
    
    engine = create_engine(CONN_STRING)
    
    # Upsert логика
    with engine.begin() as conn:
        # Временная таблица
        df.to_sql('_tmp_agg', conn, if_exists='replace', index=False)
        
        # Обновить существующие
        conn.execute("""
            UPDATE user_product_stats target
            SET total_amount = tmp.amount_sum,
                order_count = tmp.order_count,
                updated_at = NOW()
            FROM _tmp_agg tmp
            WHERE target.user_id = tmp.user_id 
              AND target.category = tmp.product_category
        """)
        
        # Вставить новые
        conn.execute("""
            INSERT INTO user_product_stats (user_id, category, total_amount, order_count)
            SELECT user_id, product_category, amount_sum, order_count
            FROM _tmp_agg tmp
            WHERE NOT EXISTS (
                SELECT 1 FROM user_product_stats target
                WHERE target.user_id = tmp.user_id 
                  AND target.category = tmp.product_category
            )
        """)
        
        conn.execute("DROP TABLE _tmp_agg")
    
    logging.info(f"Загружено {context['ti'].xcom_pull(key='result_rows')} записей")

# Определение задач
wait_for_file = FileSensor(
    task_id='wait_for_file',
    filepath=f"/data/incoming/orders_{{{{ ds }}}}.csv",
    poke_interval=60,
    timeout=7200,
    dag=dag
)

extract_task = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
validate_task = PythonOperator(task_id='validate', python_callable=validate, dag=dag)
transform_task = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
load_task = PythonOperator(task_id='load', python_callable=load, dag=dag)

# Порядок
wait_for_file >> extract_task >> validate_task >> transform_task >> load_task
```

---

### Шаг 4. Мониторинг и алерты (1 день)

#### 4.1 Логирование в Airflow

```python
import logging

def my_task(**context):
    logging.info("Начало задачи")
    logging.warning("Что-то странное, но продолжаем")
    logging.error("Критическая ошибка", exc_info=True)
```

#### 4.2 Slack алерты

```python
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

slack_alert = SlackWebhookOperator(
    task_id='slack_alert',
    http_conn_id='slack_conn',
    message=":red_circle: DAG daily_orders упал!",
    channel='#alerts',
    dag=dag
)

# В default_args
default_args = {
    'on_failure_callback': slack_alert.execute,
}
```

#### 4.3 Метрики в XCom (для дашборда)

```python
def extract(**context):
    df = pd.read_csv(...)
    context['ti'].xcom_push(key='metrics', value={
        'rows_extracted': len(df),
        'size_mb': os.path.getsize(file_path) / 1024 / 1024,
        'source': file_path
    })

# Отдельная задача для отправки метрик
def send_metrics(**context):
    metrics = context['ti'].xcom_pull(key='metrics', task_ids='extract')
    # отправить в Prometheus/CloudWatch/DataDog
```

---

### Итог Уровня 5: что реально нужно знать

| Тема | Что уметь |
|------|-----------|
| **DAG** | Создать, настроить schedule, default_args, зависимости |
| **Operators** | PythonOperator, PostgresOperator, BashOperator, FileSensor |
| **XCom** | Передавать маленькие метаданные между задачами |
| **Production** | Retry, алерты, логирование, idempotency |
| **Паттерны** | extract → validate → transform → load |

**Типичный размер DAG:** 50–150 строк кода.

**Важные правила:**
- Один DAG = один бизнес-процесс (не пихайте всё в один)
- Задачи должны быть идемпотентными
- Никаких больших данных через XCom (только пути к файлам)
- Всегда ставьте `catchup=False` для новых DAG

---

### Полный roadmap (все уровни)

| Уровень | Тема | Недель |
|---------|------|--------|
| 1 | Основы Python (структуры, файлы, try/except, logging) | 3 |
| 2 | Pandas, DuckDB, качество данных | 3 |
| 3 | Базы данных, инкременталы, SQLAlchemy | 3 |
| 4 | PySpark, Kafka, оконные функции | 4 |
| 5 | Airflow, оркестрация, production | 3 |

**Итого:** ~16 недель до уверенного Junior/Middle DE.

Успехов в переходе из BI в DE!