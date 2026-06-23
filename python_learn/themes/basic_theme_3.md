## Уровень 3: Базы данных и инкрементальная загрузка (недели 7–9)

---

### Шаг 1. Подключение к БД — SQLAlchemy (2 дня)

#### 1.1 Базовое подключение

```python
from sqlalchemy import create_engine, text
import pandas as pd

# Строка подключения: postgresql://user:pass@host:port/db
engine = create_engine('postgresql://etl_user:pass@localhost:5432/dwh')

# Чтение таблицы в pandas
df = pd.read_sql('SELECT * FROM orders WHERE date > \'2024-01-01\'', engine)

# Выполнение без извлечения данных
with engine.connect() as conn:
    conn.execute(text("DELETE FROM temp_staging"))
    conn.commit()
```

#### 1.2 Параметризованные запросы (защита от SQL injection)

```python
# Правильно
query = text("SELECT * FROM orders WHERE date > :cutoff_date")
df = pd.read_sql(query, engine, params={"cutoff_date": "2024-01-01"})

# Неправильно (опасно!)
df = pd.read_sql(f"SELECT * FROM orders WHERE date > '{cutoff_date}'", engine)
```

#### 1.3 Запись в БД

```python
# Вставка новых строк
df.to_sql('staging_orders', engine, if_exists='replace', index=False)

# Дописать (append)
df_new.to_sql('orders', engine, if_exists='append', index=False)

# chunksize для больших DataFrame (важно!)
df.to_sql('big_table', engine, if_exists='append', index=False, chunksize=10000)
```

---

### Шаг 2. Инкрементальная загрузка — ядро DE (3 дня)

#### 2.1 Простой инкрементал (по дате)

```python
def incremental_load():
    # 1. Узнаём, когда загружали в прошлый раз
    query = text("""
        SELECT COALESCE(MAX(last_loaded), '1900-01-01') as last_load
        FROM etl_metadata 
        WHERE table_name = 'orders'
    """)
    last_load = pd.read_sql(query, engine)['last_load'].iloc[0]
    
    # 2. Забираем только новое из источника
    query = text(f"""
        SELECT * FROM source_orders 
        WHERE updated_at > :last_load
    """)
    df_new = pd.read_sql(query, source_engine, params={"last_load": last_load})
    
    # 3. Вставляем в целевую таблицу
    df_new.to_sql('orders', target_engine, if_exists='append', index=False)
    
    # 4. Обновляем метаданные
    new_max = df_new['updated_at'].max()
    with target_engine.connect() as conn:
        conn.execute(text("""
            UPDATE etl_metadata 
            SET last_loaded = :new_max 
            WHERE table_name = 'orders'
        """), {"new_max": new_max})
        conn.commit()
```

#### 2.2 Upsert (обновить или вставить)

```python
def upsert(df_new, table_name, pk_columns):
    """Вставляет новые строки, обновляет существующие по PK."""
    
    # Временная таблица
    df_new.to_sql('_tmp_upsert', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        # Обновить существующие
        pk_condition = ' AND '.join([f"target.{col} = tmp.{col}" for col in pk_columns])
        set_clause = ', '.join([f"{col} = tmp.{col}" for col in df_new.columns if col not in pk_columns])
        
        conn.execute(text(f"""
            UPDATE {table_name} target
            SET {set_clause}
            FROM _tmp_upsert tmp
            WHERE {pk_condition}
        """))
        
        # Вставить новые
        conn.execute(text(f"""
            INSERT INTO {table_name}
            SELECT * FROM _tmp_upsert tmp
            WHERE NOT EXISTS (
                SELECT 1 FROM {table_name} target
                WHERE {pk_condition}
            )
        """))
        
        conn.execute(text("DROP TABLE _tmp_upsert"))
        conn.commit()
```

#### 2.3 Паттерн SCD Type 2 (храним историю изменений)

```python
def scd_type2_merge(df_new, table_name, business_key):
    """Медленно меняющееся измерение Type 2."""
    
    df_new.to_sql('_tmp_scd', engine, if_exists='replace', index=False)
    
    with engine.connect() as conn:
        # 1. Закрыть текущие записи, которые изменились
        conn.execute(text(f"""
            UPDATE {table_name} target
            SET valid_to = CURRENT_DATE, is_current = FALSE
            FROM _tmp_scd source
            WHERE target.{business_key} = source.{business_key}
              AND target.is_current = TRUE
              AND (target.name != source.name OR target.category != source.category)
        """))
        
        # 2. Вставить новые версии
        conn.execute(text(f"""
            INSERT INTO {table_name} ({', '.join(df_new.columns)})
            SELECT *, 
                   CURRENT_DATE as valid_from, 
                   '9999-12-31' as valid_to, 
                   TRUE as is_current
            FROM _tmp_scd
        """))
        
        conn.execute(text("DROP TABLE _tmp_scd"))
        conn.commit()
```

---

### Шаг 3. Обработка ошибок и транзакции (2 дня)

#### 3.1 Транзакции (всё или ничего)

```python
def safe_load():
    with engine.begin() as conn:  # Автоматический rollback при ошибке
        # Шаг 1
        conn.execute(text("DELETE FROM staging"))
        
        # Шаг 2 — если упадёт, откатятся оба шага
        conn.execute(text("INSERT INTO staging SELECT * FROM source"))
        
        # Шаг 3
        conn.execute(text("""
            INSERT INTO dim_orders
            SELECT * FROM staging
            WHERE NOT EXISTS (SELECT 1 FROM dim_orders)
        """))
        
        # Если дошли сюда — commit
```

#### 3.2 Deadlock и retry

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def load_with_retry(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
    except Exception as e:
        if 'deadlock' in str(e).lower():
            logger.warning("Deadlock, повторяем...")
            raise  # tenacity повторит
        else:
            raise  # не наша ошибка, пробрасываем
```

#### 3.3 Idempotency (повторный запуск не ломает)

```python
def idempotent_load(df, table_name, pk_columns):
    """Можно запускать сколько угодно раз — результат тот же."""
    
    with engine.begin() as conn:
        # 1. Удалить данные за этот период
        max_date = df['date'].max()
        conn.execute(text(f"""
            DELETE FROM {table_name} 
            WHERE date >= :cutoff_date
        """), {"cutoff_date": max_date - pd.Timedelta(days=1)})
        
        # 2. Вставить заново
        df.to_sql(table_name, conn, if_exists='append', index=False)
```

---

### Шаг 4. Практический мини-проект (2 дня)

**Задача:** Инкрементальная загрузка заказов из PostgreSQL в аналитическую таблицу.

```python
def daily_etl():
    logger.info("Запуск инкрементального ETL")
    
    # 1. Получить последнюю загруженную дату
    last_load = get_last_load('orders')
    logger.info(f"Последняя загрузка: {last_load}")
    
    # 2. Извлечь новые заказы
    query = text("""
        SELECT * FROM source_orders 
        WHERE updated_at > :last_load
        ORDER BY updated_at
    """)
    df_new = pd.read_sql(query, source_engine, params={"last_load": last_load})
    
    if len(df_new) == 0:
        logger.info("Нет новых данных")
        return
    
    logger.info(f"Новых записей: {len(df_new)}")
    
    # 3. Очистка и проверки
    df_new = clean_orders(df_new)
    
    # 4. Удалить дубликаты (если запустили дважды)
    with target_engine.begin() as conn:
        for order_id in df_new['order_id']:
            conn.execute(text("DELETE FROM dim_orders WHERE order_id = :oid"), 
                        {"oid": order_id})
    
    # 5. Записать
    df_new.to_sql('dim_orders', target_engine, if_exists='append', index=False)
    
    # 6. Обновить метаданные
    new_last = df_new['updated_at'].max()
    update_last_load('orders', new_last)
    
    logger.info(f"Завершено. Новый watermark: {new_last}")

def get_last_load(table_name):
    result = target_engine.execute(text("""
        SELECT COALESCE(MAX(last_loaded), '1900-01-01') as last_load
        FROM etl_control
        WHERE table_name = :tbl
    """), {"tbl": table_name}).fetchone()
    return result['last_load'] if result else '1900-01-01'
```

---

### Итог Уровня 3: что реально нужно знать

| Тема | Что уметь |
|------|-----------|
| **SQLAlchemy** | Подключение, чтение, запись, параметризованные запросы |
| **Инкрементал** | Watermark, загрузка только нового, upsert |
| **Транзакции** | `engine.begin()`, rollback при ошибке, retry при deadlock |
| **Idempotency** | Повторный запуск не дублирует данные |

**Типичный размер кода:** 80–150 строк на пайплайн.

---

Уровень 4 готовлю (PySpark, Kafka, оркестрация). Продолжаем?