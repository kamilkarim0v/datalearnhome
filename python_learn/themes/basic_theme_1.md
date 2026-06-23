Отлично. Теперь разложу **первый блок хронологии** (Уровень 1) максимально подробно — пошагово, с объяснением **зачем** это DE, а не просто "выучить синтаксис".

---

## Уровень 1: Базовый Python для DE (недели 1–3)

### Шаг 0. Установка и среда (1 день, но важен)
**Что изучить:**
- Установка Python (версия 3.10+). Совет: через `pyenv` (легко переключать версии)
- Настройка виртуального окружения: `python -m venv venv`
- Установка пакетов: `pip install` и `requirements.txt`
- **Jupyter Notebook** или **VS Code** (для DE лучше VS Code + терминал)

**Почему DE:** Вы будете запускать скрипты на серверах (Airflow, cron). Без понимания окружений начнутся конфликты библиотек.

---

### Шаг 1. Базовые структуры данных (3–4 дня)

#### 1.1 Списки (`list`)
Что изучить:
- Создание, индексация, срезы (`[start:stop:step]`)
- Методы: `.append()`, `.extend()`, `.insert()`, `.remove()`, `.pop()`, `.sort()`
- Генераторы списков: `[x*2 for x in range(10) if x > 5]`

**Пример для DE:**
```python
# Прочитать имена файлов из лога ошибок
error_files = [f"error_{i}.log" for i in range(100) if i % 10 == 0]
```

#### 1.2 Словари (`dict`)
Что изучить:
- Создание, доступ по ключу: `d['key']`, метод `.get()` (безопасный)
- Итерация: `.keys()`, `.values()`, `.items()`
- Генераторы словарей

**Пример для DE:**
```python
# Конфиг подключения к БД
db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "dwh",
    "user": os.getenv("DB_USER")
}
```

#### 1.3 Множества (`set`)
- Удаление дубликатов: `unique_ids = set(df['user_id'])`
- Операции: объединение, пересечение (`|`, `&`)

#### 1.4 Кортежи (`tuple`)
- Неизменяемые — использовать для **строк подключения**, **ключей в словаре**
- Распаковка: `host, port, db = ('localhost', 5432, 'dwh')`

**Важное отличие от BI:** В BI вы работаете с датафреймами. В DE структуры данных — это **мостик** между сырыми данными (json, строки) и аналитикой.

---

### Шаг 2. Условные операторы и циклы (2 дня)

#### 2.1 Условные операторы
- `if/elif/else`
- Тернарный оператор: `status = "ok" if row_count > 0 else "empty"`

**Для DE — проверка качества:**
```python
if df.isnull().sum().sum() > 1000:
    logging.warning("Слишком много пропусков")
    # отправить алерт или остановить пайплайн
```

#### 2.2 Циклы (особенно для файлов)
- `for item in list:` и `while`
- `break`, `continue`, `else` в циклах

**Критический пример для DE (обработка 100 CSV-файлов):**
```python
for file_path in list_of_files:
    try:
        df = pd.read_csv(file_path)
        # ... обработать
    except pd.errors.EmptyDataError:
        logging.error(f"Пустой файл: {file_path}")
        continue  # пропустить, идти дальше
```

---

### Шаг 3. Функции (2 дня) — но не декораторы еще

#### 3.1 Определение и вызов
- `def`, `return`, параметры (позиционные, именованные, значения по умолчанию)
- `*args` и `**kwargs` (полезно для оберток подключений)

#### 3.2 Docstring и аннотации типов (важно для DE!)
```python
def read_table(
    connection_string: str,
    table_name: str,
    limit: int = 1000
) -> pd.DataFrame:
    """Читает таблицу из БД с лимитом"""
    ...
```
В DE функции будут вызывать другие DE-инженеры. Без аннотаций — chaos.

#### 3.3 Генераторы (`yield`) — ключевая тема для DE
**Зачем:** Экономия памяти при обработке больших файлов (10+ ГБ).

**Пример: читать большой CSV построчно, не загружая в память**
```python
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip().split(',')

# Использование
for row in read_large_file("big_data.csv"):
    process_row(row)  # не храним весь файл
```

**Итераторы** — по сути то же, но через `__iter__` и `__next__` (редко нужно в DE).

**Декораторы** оставьте на уровень 3–4 (нужны для ретраев, логирования в Airflow).

---

### Шаг 4. Try/Except (1.5 дня) — углубленно

#### 4.1 Конкретные типы исключений (а не голый `except:`)
```python
try:
    conn = psycopg2.connect(**db_config)
    df = pd.read_sql("SELECT * FROM huge_table", conn)
except psycopg2.OperationalError as e:
    logging.error(f"БД недоступна: {e}")
    # retry логика
    raise  # если хотим остановить пайплайн
except MemoryError:
    logging.critical("Не хватает памяти, нужно читать с chunksize")
    # переключиться на построчную обработку
except Exception as e:
    logging.exception("Неожиданная ошибка")
    raise
```

#### 4.2 `else` и `finally`
```python
try:
    file = open("data.csv")
except FileNotFoundError:
    logging.warning("Файл не найден, пропускаем")
else:
    # выполнится, если не было исключения
    data = file.read()
finally:
    # всегда закрываем файл
    file.close()
```

#### 4.3 Паттерн retry (полезно для внешних API/БД)
```python
import time
for attempt in range(3):
    try:
        df = pd.read_csv("http://api/data.csv")
        break
    except Exception as e:
        logging.warning(f"Попытка {attempt+1} провалилась")
        time.sleep(2 ** attempt)  # exponential backoff
else:
    raise Exception("Не удалось после 3 попыток")
```

---

### Шаг 5. Работа с файлами (3 дня) — фундамент для Extract

#### 5.1 Базовое открытие (`open`, `with`)
```python
with open("log.txt", "a") as f:
    f.write(f"{datetime.now()}: Загрузка завершена\n")
```

#### 5.2 Работа с CSV (встроенный модуль `csv`)
```python
import csv
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)  # сразу в словари
    for row in reader:
        print(row["user_id"], row["amount"])
```

**Почему не pandas везде:** Pandas грузит всё в RAM. Для файлов >5 ГБ на слабом сервере — крах. А `csv.reader` + генератор — выживет.

#### 5.3 Работа с JSON (строки и файлы)
```python
import json
# Чтение
with open("config.json") as f:
    config = json.load(f)

# Запись
with open("result.json", "w") as f:
    json.dump(output_data, f, indent=2)

# Потоковый JSON (каждый объект на отдельной строке)
with open("big.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)
        process(obj)
```

#### 5.4 Формат Parquet (через `pandas` или `pyarrow`)
```python
# Чтение
df = pd.read_parquet("data.parquet")

# Запись (экономит место, быстрее CSV)
df.to_parquet("output.parquet", compression="snappy")
```
**Для DE:** Parquet — стандарт в Data Lake. Колоночный, сжатый, со схемой.

---

### Шаг 6. Логирование (`logging`) — 2 дня (делайте сразу правильно)

#### 6.1 Базовая настройка
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()  # в консоль
    ]
)

logger = logging.getLogger(__name__)
```

#### 6.2 Уровни логирования для DE
```python
logger.debug("Детали для отладки")      # временные проверки
logger.info("Загружено 5000 строк")     # нормальный ход
logger.warning("Пропущена 1 пустая строка")  # ошибки, но пайплайн жив
logger.error("Не удалось подключиться к БД")  # серьёзно
logger.critical("Нет места на диске")   # всё падает
```

#### 6.3 Что обязательно логировать в DE пайплайне
- **Начало и конец этапа:** `Запуск extract из source A`, `Завершено за 12.3 сек`
- **Статус:** `Строк прочитано: 10000`, `Строк записано: 9995`
- **Ошибки с контекстом:**
```python
try:
    df = pd.read_csv(path)
except Exception as e:
    logger.exception(f"Ошибка чтения {path}: {e}")
    # exception() автоматически добавит traceback
```
- **Метрики качества:** `Найдено 150 дубликатов по user_id`

#### 6.4 RotatingFileHandler (чтобы лог не вырос до 100 ГБ)
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "etl.log", maxBytes=10_000_000, backupCount=5
)
```

---

## ✅ Что вы умеете после Уровня 1:

1. Создавать скрипт, который:
   - Читает конфиг из JSON/.env
   - Открывает CSV/JSON/Parquet
   - Обрабатывает ошибки (файл не найден, пустой, битый)
   - Пишет подробный лог с ротацией
   - Не падает от единичной ошибки (continue/retry)

2. Понимаете, когда использовать список/словарь/генератор

3. Можете прочитать большой файл **построчно** без загрузки в память

**Пример задачи на конец уровня 1:**
> Напишите скрипт, который рекурсивно обходит папку `incoming`, читает все `.csv` файлы (даже если некоторые повреждены), пишет в один общий Parquet-файл и логирует каждое действие (имя файла, кол-во строк, ошибки).

---

## Следующий шаг (Уровень 2)

После этого переходите к **Pandas + DuckDB** (я распишу так же детально, если попросите). Но сначала полностью закрепите Уровень 1 — это **китчевый фундамент**, на котором держится всё остальное. Без него PySpark и Kafka превратятся в "магию, которая не работает".