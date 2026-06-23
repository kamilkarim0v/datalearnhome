## Уровень 4: Большие данные — PySpark и потоковая обработка (недели 10–14)

---

### Шаг 1. PySpark — фундамент (4 дня)

#### 1.1 Запуск и базовые понятия

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Создание сессии (одна на приложение)
spark = SparkSession.builder \
    .appName("my_etl") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# DataFrame vs RDD (вам нужен DataFrame, RDD — редко)
```

#### 1.2 Чтение данных

```python
# Из файлов (автоматически партиционирует)
df = spark.read.parquet("s3://bucket/sales/*.parquet")
df = spark.read.csv("path/to/files/", header=True, inferSchema=True)
df = spark.read.json("logs/*.jsonl")

# Из PostgreSQL (тяжело, лучше через экспорт в Parquet)
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/db") \
    .option("dbtable", "orders") \
    .option("user", "user") \
    .option("password", "pass") \
    .load()

# Из Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders-topic") \
    .load()
```

#### 1.3 Трансформации (похоже на Pandas, но lazy)

```python
# Базовые операции
df_filtered = df.filter(col("amount") > 1000)
df_selected = df.select("user_id", "amount", "date")

# Новые колонки
df_with_tax = df.withColumn("tax", col("amount") * 0.2)
df_with_flag = df.withColumn("is_high", when(col("amount") > 10000, 1).otherwise(0))

# Группировка
df_grouped = df.groupBy("region", "category").agg(
    sum("amount").alias("total_sales"),
    count("user_id").alias("unique_users"),
    avg("amount").alias("avg_amount")
)

# Join (осторожно — вызывает shuffle!)
df_joined = df_orders.join(df_users, on="user_id", how="left")
```

#### 1.4 Оптимизации (ключевое отличие от Pandas)

```python
# 1. Lazy evaluation — ничего не выполняется, пока не вызвали action
df_transformed = df.filter(...).groupBy(...).agg(...)  # ничего не произошло

# 2. Action — только тут начинается работа
result = df_transformed.collect()  # в память драйвера (опасно!)
result = df_transformed.count()    # просто число
df_transformed.write.parquet("output/")  # запись

# 3. Репартиционирование перед join (если таблицы большие)
df_orders = df_orders.repartition(200, "user_id")
df_users = df_users.repartition(200, "user_id")  # тот же ключ — дешевле join

# 4. Broadcast маленькой таблицы (как в DuckDB)
from pyspark.sql.functions import broadcast
df_joined = df_orders.join(broadcast(df_users), on="user_id")
```

#### 1.5 Запись результатов

```python
# Parquet — стандарт (автоматическая партиция)
df.write.mode("overwrite").parquet("output/")

# С партиционированием
df.write \
    .partitionBy("year", "month") \
    .mode("append") \
    .parquet("lake/orders/")

# В PostgreSQL (медленно, лучше Parquet + внешняя таблица)
df.write \
    .mode("append") \
    .jdbc("jdbc:postgresql://localhost/db", "target_table",
          properties={"user": "user", "password": "pass"})
```

---

### Шаг 2. Водяные знаки и оконные функции (1 день)

#### 2.1 Window functions в Spark (аналог SQL)

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, lag, lead, sum as spark_sum

# Окно
window_spec = Window.partitionBy("user_id").orderBy("date")

# Номер строки в группе
df = df.withColumn("rn", row_number().over(window_spec))

# Лаг (предыдущее значение)
df = df.withColumn("prev_amount", lag("amount", 1).over(window_spec))

# Накопленная сумма
df = df.withColumn("running_total", spark_sum("amount").over(window_spec.rowsBetween(-6, 0)))
```

#### 2.2 Водяной знак для потоковой обработки

```python
# Для структурированного стриминга
from pyspark.sql.functions import window

df_stream = spark.readStream \
    .format("kafka") \
    .option("subscribe", "topic") \
    .load() \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Окно с водяным знаком (допускает опоздания до 10 минут)
result = df_stream \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    ).agg(sum("amount").alias("total"))
```

---

### Шаг 3. Spark SQL — если привыкли к SQL (1 день)

```python
# Регистрируем DataFrame как временное представление
df.createOrReplaceTempView("orders")
df_users.createOrReplaceTempView("users")

# Пишем SQL
result = spark.sql("""
    SELECT 
        o.region,
        DATE_TRUNC('month', o.date) as month,
        SUM(o.amount) as revenue,
        COUNT(DISTINCT o.user_id) as users
    FROM orders o
    LEFT JOIN users u ON o.user_id = u.id
    WHERE o.amount > 0
    GROUP BY o.region, month
    HAVING revenue > 10000
    ORDER BY month DESC
""")

result.write.parquet("aggregated/")
```

---

### Шаг 4. Практический мини-проект (3 дня)

**Задача:** PySpark ETL из S3 в S3 с агрегацией.

```python
def pyspark_etl():
    spark = SparkSession.builder.appName("daily_aggregator").getOrCreate()
    
    # 1. Extract — читаем сырые данные
    df_raw = spark.read.parquet("s3://raw/sales/*.parquet")
    
    # 2. Basic cleaning
    df_clean = df_raw \
        .filter(col("amount") > 0) \
        .filter(col("user_id").isNotNull()) \
        .withColumn("date", to_date(col("timestamp"))) \
        .withColumn("year", year("date")) \
        .withColumn("month", month("date"))
    
    # 3. Remove duplicates (keep latest by timestamp)
    window_spec = Window.partitionBy("order_id").orderBy(col("timestamp").desc())
    df_unique = df_clean \
        .withColumn("rn", row_number().over(window_spec)) \
        .filter(col("rn") == 1) \
        .drop("rn")
    
    # 4. Join with small dimension (broadcast)
    df_users = spark.read.parquet("s3://dim/users.parquet")
    df_enriched = df_unique.join(broadcast(df_users), on="user_id", how="left")
    
    # 5. Daily aggregation
    df_daily = df_enriched \
        .groupBy("date", "region", "product_category") \
        .agg(
            sum("amount").alias("revenue"),
            countDistinct("user_id").alias("unique_users"),
            count("order_id").alias("orders_count")
        )
    
    # 6. Write with partitioning
    df_daily.write \
        .partitionBy("date") \
        .mode("overwrite") \
        .parquet("s3://gold/daily_sales/")
    
    # 7. Log metrics
    row_count = df_daily.count()
    print(f"Written {row_count} rows")
    
    spark.stop()
```

---

### Шаг 5. Kafka — потоковая обработка (2 дня)

#### 5.1 Consumer (чтение)

```python
# batch чтение (не потоковое)
df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING) as json") \
    .select(from_json("json", schema).alias("data")) \
    .select("data.*")

# потоковое чтение (streaming)
stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .load()
```

#### 5.2 Streaming aggregation

```python
# 5-минутные окна
result_stream = stream \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*") \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    ).agg(sum("amount").alias("total"))

# Запись потока в консоль (для отладки)
query = result_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Запись в Parquet (чекапойнт для восстановления)
query = result_stream.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "s3://output/") \
    .option("checkpointLocation", "s3://checkpoints/") \
    .start()

query.awaitTermination()
```

---

### Итог Уровня 4: что реально нужно знать

| Тема | Что уметь |
|------|-----------|
| **PySpark DataFrame** | Чтение/запись, фильтрация, groupBy, join, withColumn |
| **Оптимизация** | Lazy evaluation, broadcast join, репартиционирование |
| **Spark SQL** | Регистрация таблиц, SQL-запросы вместо DataFrame API |
| **Window functions** | row_number, lag, running_total в Spark |
| **Kafka streaming** | Чтение топика, watermark, окна, запись результата |

**Типичный размер кода:** 100–200 строк на ETL.

**Важное отличие от Уровня 3:** 
- Spark работает с **кластером**, а не одной машиной
- Данные не помещаются в RAM одной машины (терабайты)
- Код lazy — выполняется только при action или записи

---

Уровень 5 готовлю (Airflow, оркестрация, CI/CD для DE). Продолжаем?