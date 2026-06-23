Договорились. Давайте **Уровень 2** — сжато, но с конкретикой. Без воды, но с примерами, которые реально пригодятся.

---

## Уровень 2: Обработка и трансформация данных (недели 4–6)

---

### Шаг 1. Pandas для DE — только нужное (3 дня)

#### 1.1 Чтение с контролем памяти (критично)

```python
# Паттерн для больших файлов
chunksize = 100000  # строк за раз
writer = None

for chunk in pd.read_csv('huge_file.csv', chunksize=chunksize):
    chunk['processed_date'] = pd.Timestamp.now()
    
    if writer is None:
        writer = pd.DataFrame.to_parquet(chunk, 'output.parquet', engine='pyarrow')
    else:
        writer.write_table(chunk)
```

#### 1.2 Трансформации (ваш BI-опыт переезжает)

```python
# Фильтрация
df = df[df['amount'] > 0]

# Новые колонки
df['amount_usd'] = df['amount'] * df['rate']

# Агрегация
df_grouped = df.groupby(['region', 'category'], as_index=False).agg({
    'amount': 'sum',
    'user_id': 'nunique',
    'order_id': 'count'
})

# Join
df_enriched = df_orders.merge(df_users, on='user_id', how='left')

# Очистка дубликатов
df = df.drop_duplicates(subset=['order_id'], keep='last')
```

#### 1.3 Работа с датами (95% пайплайнов)

```python
# Конвертация
df['date'] = pd.to_datetime(df['date_str'])

# Фильтр по дате (инкрементальная загрузка)
last_load = '2024-01-01'
df_new = df[df['date'] > last_load]

# Извлечение компонентов
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Лаг (разница с предыдущим)
df['prev_amount'] = df.groupby('user_id')['amount'].shift(1)
df['change'] = df['amount'] - df['prev_amount']
```

#### 1.4 Запись результатов

```python
# В Parquet (всегда предпочтительнее CSV)
df.to_parquet('clean_data.parquet', compression='snappy', index=False)

# С партиционированием (ускоряет чтение)
df.to_parquet('lake/', partition_cols=['year', 'month'])

# В CSV (только если просит бизнес)
df.to_csv('report.csv', index=False, encoding='utf-8-sig')
```

---

### Шаг 2. DuckDB — когда памяти не хватает (1.5 дня)

#### 2.1 Когда использовать

| Ситуация | Решение |
|----------|---------|
| Данные до 2-3 ГБ | Pandas |
| Данные 3-50 ГБ или сложные джойны | DuckDB |
| Нужен SQL вместо Python | DuckDB |

#### 2.2 Базовый паттерн

```python
import duckdb

# SQL прямо на файлах (не загружая в память)
result = duckdb.query("""
    SELECT 
        region,
        DATE_TRUNC('month', date) as month,
        SUM(amount) as total_sales,
        COUNT(DISTINCT user_id) as unique_users
    FROM 'sales/*.parquet'
    WHERE amount > 0
    GROUP BY region, month
    ORDER BY month DESC
""").fetchdf()  # результат — Pandas DataFrame
```

#### 2.3 Реальный пример (инкрементальный пайплайн)

```python
def transform_with_duckdb():
    conn = duckdb.connect(':memory:')
    
    # 1. Читаем новые данные
    conn.execute("CREATE VIEW new_data AS SELECT * FROM read_csv('incoming/*.csv')")
    
    # 2. Джойним с историей
    conn.execute("""
        CREATE OR REPLACE TABLE enriched AS
        SELECT 
            n.*,
            h.user_name,
            h.region
        FROM new_data n
        LEFT JOIN read_parquet('history/users.parquet') h 
            ON n.user_id = h.user_id
    """)
    
    # 3. Агрегируем
    result = conn.execute("""
        SELECT 
            region,
            DATE_TRUNC('day', date) as day,
            SUM(amount) as daily_amount
        FROM enriched
        GROUP BY region, day
    """).fetchdf()
    
    return result
```

#### 2.4 Оконные функции (которые в Pandas мучительно делать)

```python
# Скользящее среднее за 7 дней
windowed = duckdb.query("""
    SELECT 
        date,
        amount,
        AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma7,
        LAG(amount, 1) OVER (ORDER BY date) as prev_amount
    FROM 'sales.parquet'
""").fetchdf()
```

---

### Шаг 3. Качество данных (1.5 дня)

#### 3.1 Чеклист проверок (копируйте в проект)

```python
def quality_checks(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Применяет стандартные проверки. Возвращает очищенный df."""
    
    # 1. Пустой датафрейм
    if len(df) == 0:
        raise ValueError(f"{table_name}: пустой датафрейм")
    
    # 2. Null в ключевых полях
    critical_cols = ['user_id', 'date', 'amount']
    for col in critical_cols:
        null_cnt = df[col].isna().sum()
        if null_cnt > 0:
            logger.error(f"{col}: {null_cnt} null значений")
            # Удаляем строки с null в ключевых полях
            df = df[df[col].notna()]
    
    # 3. Дубликаты по первичному ключу
    pk_cols = ['user_id', 'date']
    dupes = df.duplicated(subset=pk_cols).sum()
    if dupes > 0:
        logger.warning(f"{dupes} дубликатов, оставляем последний")
        df = df.drop_duplicates(subset=pk_cols, keep='last')
    
    # 4. Диапазоны значений
    if df['amount'].min() < 0:
        logger.error(f"Отрицательные суммы: {df[df['amount'] < 0]['amount'].tolist()[:5]}")
        df = df[df['amount'] >= 0]
    
    # 5. Ожидаемые категории
    if 'category' in df.columns:
        expected = ['A', 'B', 'C']
        invalid = df[~df['category'].isin(expected)]
        if len(invalid) > 0:
            logger.error(f"Неизвестные категории: {invalid['category'].unique()}")
            df = df[df['category'].isin(expected)]
    
    logger.info(f"{table_name}: после очистки {len(df)} строк")
    return df
```

#### 3.2 Аномалии (ловит сломанный пайплайн)

```python
def anomaly_detection(df: pd.DataFrame, historical_mean: float):
    """Проверяет, не упало/выросло ли среднее аномально."""
    current_mean = df['amount'].mean()
    deviation = abs(current_mean - historical_mean) / historical_mean
    
    if deviation > 0.3:  # изменилось более чем на 30%
        logger.error(f"Аномалия: среднее {current_mean:.2f} vs история {historical_mean:.2f}")
        # Можно отправить алерт в Telegram/Slack
        return False
    return True
```

#### 3.3 Схема данных (если источник изменил структуру)

```python
expected_schema = {
    'user_id': 'int64',
    'amount': 'float64',
    'date': 'datetime64[ns]',
    'category': 'object'
}

for col, dtype in expected_schema.items():
    if col not in df.columns:
        raise ValueError(f"Колонка {col} отсутствует")
    if str(df[col].dtype) != dtype:
        logger.warning(f"Тип {col}: ожидался {dtype}, получен {df[col].dtype}")
```

---

### Шаг 4. Polars — на будущее (1 день, опционально)

**Почему стоит знать:** Быстрее Pandas в 5-10 раз, автоматическая параллелизация.

**Базовый паттерн (заменитель Pandas):**
```python
import polars as pl

# Чтение
df = pl.read_csv("data.csv")

# Трансформации (цепочка методов)
result = (df
    .filter(pl.col("amount") > 0)
    .with_columns([
        (pl.col("amount") * pl.col("rate")).alias("amount_usd"),
        pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")
    ])
    .group_by("region")
    .agg([
        pl.col("amount").sum(),
        pl.col("user_id").n_unique()
    ])
)

# В Pandas (если нужно сдать в другой инструмент)
df_pandas = result.to_pandas()
```

**Когда переходить с Pandas на Polars:**
- Данные > 5 ГБ и медленно
- У вас много CPU (Polars параллелит автоматически)
- Вы готовы учить новый синтаксис

---

### Шаг 5. Сквозной проект (1 день)

**Задача:** Обработать логи продаж из 10 CSV файлов.

```python
def etl_pipeline():
    logger.info("Запуск ETL")
    
    # 1. Extract — чтение всех файлов
    all_dfs = []
    for file in glob.glob("raw/sales_*.csv"):
        try:
            df = pd.read_csv(file)
            logger.info(f"Прочитан {file}: {len(df)} строк")
            all_dfs.append(df)
        except Exception as e:
            logger.error(f"Ошибка {file}: {e}")
    
    df = pd.concat(all_dfs, ignore_index=True)
    
    # 2. Quality — проверки
    df = quality_checks(df, "sales")
    
    # 3. Transform
    if len(df) > 1_000_000:
        # DuckDB для больших данных
        result = duckdb.query("""
            SELECT 
                DATE_TRUNC('day', date) as sale_date,
                category,
                SUM(amount) as revenue,
                COUNT(*) as transactions
            FROM df
            GROUP BY sale_date, category
        """).fetchdf()
    else:
        # Pandas для маленьких
        result = df.groupby([pd.Grouper(key='date', freq='D'), 'category']).agg(
            revenue=('amount', 'sum'),
            transactions=('order_id', 'count')
        ).reset_index()
    
    # 4. Load — запись с партициями
    result['year'] = result['sale_date'].dt.year
    result['month'] = result['sale_date'].dt.month
    result.to_parquet(
        "gold/sales_aggregated.parquet",
        partition_cols=['year', 'month'],
        compression='snappy'
    )
    
    logger.info(f"Записано {len(result)} строк в gold/ в")
    return gold/ result
```

---


## Итог Уровня 2: что реально нужно знать

| Тема | Что уметь |
|------|-----------|
| **Pandas** | `chunksize`, группировки, джойны, даты, запись в Parquet |
| **DuckDB** | Написать SELECT на файлах, оконные функции, замена Pandas при нехватке памяти |
| **Quality** | 5 проверок: пустой, null в ключах, дубликаты, диапазоны, категории |
| **Polars** | Опционально — ускоритель вместо Pandas для больших данных |

**Типичный размер кода на проект:** 50–100 строк на ETL.

---

Уровень 3 готовлю (БД, инкрементальная загрузка, SQLAlchemy). Продолжаем?