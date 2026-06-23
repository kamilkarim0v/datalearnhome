Отличный вопрос! Давайте разберем все способы преобразования строки в ISO формат даты.

## 1. Базовое преобразование строки в ISO формат

```python
from datetime import datetime
import pytz
from zoneinfo import ZoneInfo

# ===== ИСХОДНАЯ СТРОКА =====
date_string = '2026-01-01'

# ===== СПОСОБ 1: Простое преобразование =====
# Преобразуем строку в объект datetime
dt = datetime.fromisoformat(date_string)
# Теперь преобразуем обратно в ISO строку
iso_string = dt.isoformat()
print(iso_string)  # '2026-01-01T00:00:00'

# ===== СПОСОБ 2: С указанием времени =====
dt = datetime.strptime(date_string, '%Y-%m-%d')
iso_string = dt.isoformat()
print(iso_string)  # '2026-01-01T00:00:00'

# ===== СПОСОБ 3: С часовым поясом UTC =====
dt = datetime.fromisoformat(date_string).replace(tzinfo=pytz.UTC)
iso_string = dt.isoformat()
print(iso_string)  # '2026-01-01T00:00:00+00:00'

# ===== СПОСОБ 4: Без преобразования в объект (прямая конкатенация) =====
iso_string = date_string + 'T00:00:00+00:00'
print(iso_string)  # '2026-01-01T00:00:00+00:00'
```

## 2. Различные варианты ISO формата

```python
from datetime import datetime, timezone, timedelta
import pytz

date_string = '2026-01-01'

# ===== ВАРИАНТЫ ISO ФОРМАТА =====

# 1. Базовый ISO (без времени)
dt = datetime.fromisoformat(date_string)
print(dt.isoformat())  # '2026-01-01T00:00:00'

# 2. Только дата в ISO формате
print(dt.date().isoformat())  # '2026-01-01'

# 3. С миллисекундами
print(dt.isoformat(timespec='milliseconds'))  # '2026-01-01T00:00:00.000'

# 4. С микросекундами
print(dt.isoformat(timespec='microseconds'))  # '2026-01-01T00:00:00.000000'

# 5. Без времени (только дата)
print(dt.isoformat(timespec='hours'))  # '2026-01-01T00'

# 6. С UTC часовым поясом
dt_utc = dt.replace(tzinfo=timezone.utc)
print(dt_utc.isoformat())  # '2026-01-01T00:00:00+00:00'

# 7. С конкретным часовым поясом
dt_moscow = dt.replace(tzinfo=pytz.timezone('Europe/Moscow'))
print(dt_moscow.isoformat())  # '2026-01-01T00:00:00+03:00'

# 8. Кастомный разделитель
print(dt.isoformat().replace('T', ' '))  # '2026-01-01 00:00:00'

# 9. Без микросекунд (для API)
print(dt.isoformat(timespec='seconds'))  # '2026-01-01T00:00:00'

# 10. Полный формат с Z (UTC)
dt_utc = datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
print(dt_utc.isoformat().replace('+00:00', 'Z'))  # '2026-01-01T00:00:00Z'
```

## 3. Для Tinkoff API (специфичные форматы)

```python
from datetime import datetime, timezone, timedelta

# ===== ФОРМАТЫ ДЛЯ TINKOFF API =====

def to_tinkoff_format(date_string: str, with_time: bool = True) -> str:
    """
    Преобразование в формат для Tinkoff API
    
    Args:
        date_string: строка даты 'YYYY-MM-DD'
        with_time: добавить время (00:00:00) или только дату
    """
    dt = datetime.fromisoformat(date_string)
    dt_utc = dt.replace(tzinfo=timezone.utc)
    
    if with_time:
        return dt_utc.isoformat()  # '2026-01-01T00:00:00+00:00'
    else:
        return dt_utc.date().isoformat()  # '2026-01-01'

# Примеры для Tinkoff API
date_string = '2026-01-01'

# Вариант 1: Полный ISO с UTC (рекомендуемый для Tinkoff)
dt = datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
tinkoff_format = dt.isoformat()
print(tinkoff_format)  # '2026-01-01T00:00:00+00:00'

# Вариант 2: С Z вместо +00:00
tinkoff_format_z = dt.isoformat().replace('+00:00', 'Z')
print(tinkoff_format_z)  # '2026-01-01T00:00:00Z'

# Вариант 3: Для from/to в GetCandles (нужно время)
now = datetime.now(timezone.utc)
from_date = datetime.fromisoformat('2026-01-01').replace(tzinfo=timezone.utc)

data = {
    "figi": "BBG004730N88",
    "from": from_date.isoformat(),  # '2026-01-01T00:00:00+00:00'
    "to": now.isoformat(),          # текущее время
    "interval": "CANDLE_INTERVAL_15_MIN"
}
```

## 4. Универсальная функция для преобразования

```python
from datetime import datetime, timezone
from typing import Optional, Literal

def to_iso_format(
    date_string: str,
    timezone_offset: Optional[str] = None,
    format_type: Literal['full', 'date', 'time', 'zulu'] = 'full',
    timespec: str = 'seconds'
) -> str:
    """
    Универсальное преобразование строки даты в ISO формат
    
    Args:
        date_string: строка даты 'YYYY-MM-DD'
        timezone_offset: часовой пояс '+00:00', '+03:00' и т.д.
        format_type: 'full' - полный, 'date' - только дата, 
                    'time' - только время, 'zulu' - с Z
        timespec: точность времени ('hours', 'minutes', 'seconds', 'milliseconds')
    
    Returns:
        Строка в ISO формате
    """
    # Преобразуем строку в datetime
    dt = datetime.fromisoformat(date_string)
    
    # Добавляем часовой пояс
    if timezone_offset:
        # Парсим смещение
        hours, minutes = map(int, timezone_offset.split(':'))
        tz = timezone(timedelta(hours=hours, minutes=minutes))
        dt = dt.replace(tzinfo=tz)
    else:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Форматируем в зависимости от типа
    if format_type == 'date':
        return dt.date().isoformat()
    
    elif format_type == 'time':
        return dt.time().isoformat()
    
    elif format_type == 'zulu':
        return dt.isoformat(timespec=timespec).replace('+00:00', 'Z')
    
    else:  # full
        return dt.isoformat(timespec=timespec)

# ===== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ =====

date_str = '2026-01-01'

# Базовый ISO
print(to_iso_format(date_str))
# '2026-01-01T00:00:00+00:00'

# Только дата
print(to_iso_format(date_str, format_type='date'))
# '2026-01-01'

# С Z вместо +00:00
print(to_iso_format(date_str, format_type='zulu'))
# '2026-01-01T00:00:00Z'

# С московским временем
print(to_iso_format(date_str, timezone_offset='+03:00'))
# '2026-01-01T00:00:00+03:00'

# С миллисекундами
print(to_iso_format(date_str, timespec='milliseconds'))
# '2026-01-01T00:00:00.000+00:00'

# Без времени (только дата для SQL)
print(to_iso_format(date_str, format_type='date'))
# '2026-01-01'
```

## 5. Работа с разными входными форматами

```python
from datetime import datetime
from dateutil import parser  # pip install python-dateutil

# ===== РАЗНЫЕ ВХОДНЫЕ ФОРМАТЫ =====

date_strings = [
    '2026-01-01',
    '2026-01-01 12:30:00',
    '01/01/2026',
    '1 Jan 2026',
    '2026-01-01T12:30:00+00:00'
]

def parse_to_iso(date_str: str) -> str:
    """Парсинг разных форматов в ISO"""
    try:
        # Способ 1: Попробовать стандартный парсинг
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str)
        else:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            # Способ 2: Использовать dateutil (поддерживает много форматов)
            dt = parser.parse(date_str)
        except:
            raise ValueError(f"Неизвестный формат даты: {date_str}")
    
    # Добавляем UTC если нет часового пояса
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.isoformat()

# Примеры
for s in date_strings:
    print(f"{s} -> {parse_to_iso(s)}")
```

## 6. Для работы с БД (SQL)

```python
from datetime import datetime, timezone

date_string = '2026-01-01'

# ===== ДЛЯ POSTGRESQL =====

# 1. TIMESTAMP без часового пояса
dt = datetime.fromisoformat(date_string)
postgres_format = dt.isoformat(sep=' ', timespec='seconds')
print(postgres_format)  # '2026-01-01 00:00:00'

# 2. TIMESTAMP с часовым поясом
dt_utc = datetime.fromisoformat(date_string).replace(tzinfo=timezone.utc)
postgres_tz_format = dt_utc.isoformat(sep=' ', timespec='seconds')
print(postgres_tz_format)  # '2026-01-01 00:00:00+00:00'

# 3. Для SQL запроса (без времени)
sql_date = datetime.fromisoformat(date_string).date()
print(sql_date)  # '2026-01-01'

# ===== ДЛЯ SQLITE =====

# SQLite принимает ISO форматы
sqlite_format = datetime.fromisoformat(date_string).isoformat()
print(sqlite_format)  # '2026-01-01T00:00:00'

# ===== ДЛЯ MYSQL =====

mysql_format = datetime.fromisoformat(date_string).strftime('%Y-%m-%d %H:%M:%S')
print(mysql_format)  # '2026-01-01 00:00:00'
```

## 7. Практический пример для Tinkoff API с запросом за период

```python
from datetime import datetime, timezone, timedelta
import requests
import json

class TinkoffDateConverter:
    @staticmethod
    def to_api_format(date_string: str) -> str:
        """Преобразование даты в формат для Tinkoff API"""
        dt = datetime.fromisoformat(date_string)
        dt_utc = dt.replace(tzinfo=timezone.utc)
        return dt_utc.isoformat()
    
    @staticmethod
    def get_date_range(from_date: str, to_date: str) -> dict:
        """Получение диапазона дат для API"""
        return {
            "from": TinkoffDateConverter.to_api_format(from_date),
            "to": TinkoffDateConverter.to_api_format(to_date)
        }

# Пример использования
converter = TinkoffDateConverter()

# Запрос за конкретную дату
date_range = converter.get_date_range('2026-01-01', '2026-01-02')

data = {
    "figi": "BBG004730N88",
    **date_range,  # распаковываем from и to
    "interval": "CANDLE_INTERVAL_15_MIN"
}

print(json.dumps(data, indent=2))
# Результат:
# {
#   "figi": "BBG004730N88",
#   "from": "2026-01-01T00:00:00+00:00",
#   "to": "2026-01-02T00:00:00+00:00",
#   "interval": "CANDLE_INTERVAL_15_MIN"
# }
```

## 8. Шпаргалка по преобразованиям

```python
# ===== ШПАРГАЛКА =====

date_str = '2026-01-01'

# --- Простые преобразования ---
# 1. В datetime
dt = datetime.fromisoformat(date_str)  # datetime(2026, 1, 1, 0, 0)

# 2. В ISO строку
iso = dt.isoformat()  # '2026-01-01T00:00:00'

# 3. В ISO с UTC
iso_utc = dt.replace(tzinfo=timezone.utc).isoformat()  # '2026-01-01T00:00:00+00:00'

# 4. В ISO с Z
iso_z = dt.replace(tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')  # '2026-01-01T00:00:00Z'

# --- Для Tinkoff API ---
# 5. Формат from/to (нужно время)
from_date = datetime.fromisoformat('2026-01-01').replace(tzinfo=timezone.utc)
to_date = datetime.now(timezone.utc)

data = {
    "from": from_date.isoformat(),
    "to": to_date.isoformat()
}

# --- Для SQL ---
# 6. PostgreSQL
sql_ts = dt.isoformat(sep=' ', timespec='seconds')  # '2026-01-01 00:00:00'

# 7. MySQL
sql_mysql = dt.strftime('%Y-%m-%d %H:%M:%S')  # '2026-01-01 00:00:00'

# --- Для URL параметров ---
# 8. URL encoded
url_param = dt.isoformat().replace('+', '%2B')  # '2026-01-01T00%3A00%3A00%2B00%3A00'
```

Выбирайте подходящий способ в зависимости от того, куда вы отправляете данные и какой формат ожидает получатель!