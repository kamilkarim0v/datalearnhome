Вот полный список всех методов словарей (dict) в Python:

## Базовые методы

| Метод | Описание | Пример |
|-------|----------|--------|
| `clear()` | Удаляет все элементы из словаря | `d.clear()` |
| `copy()` | Возвращает поверхностную копию словаря | `d2 = d.copy()` |
| `fromkeys(iterable, value)` | Создает новый словарь из ключей с одинаковым значением | `dict.fromkeys(['a','b'], 0)` |

## Методы для доступа к данным

| Метод | Описание | Пример |
|-------|----------|--------|
| `get(key, default)` | Возвращает значение по ключу (или default, если ключа нет) | `d.get('key', 'not found')` |
| `setdefault(key, default)` | Возвращает значение или устанавливает default, если ключа нет | `d.setdefault('new', [])` |
| `keys()` | Возвращает view объектов ключей | `d.keys()` |
| `values()` | Возвращает view объектов значений | `d.values()` |
| `items()` | Возвращает view пар (ключ, значение) | `d.items()` |

## Методы для изменения данных

| Метод | Описание | Пример |
|-------|----------|--------|
| `update(other)` | Обновляет словарь из другого словаря/итератора | `d.update({'x': 1})` |
| `pop(key, default)` | Удаляет ключ и возвращает значение (KeyError если нет) | `d.pop('key')` |
| `popitem()` | Удаляет и возвращает последнюю добавленную пару (Python 3.7+) | `d.popitem()` |

## Примеры использования:

```python
# Создание словаря
d = {'a': 1, 'b': 2, 'c': 3}

# Базовые операции
d.clear()                     # {}
d2 = d.copy()                 # {'a': 1, 'b': 2, 'c': 3}

# fromkeys - создание словаря с одинаковыми значениями
keys = ['name', 'age', 'city']
new_dict = dict.fromkeys(keys, 'unknown')  # {'name': 'unknown', 'age': 'unknown', 'city': 'unknown'}

# get - безопасное получение значения
print(d.get('a'))             # 1
print(d.get('z'))             # None
print(d.get('z', 'default'))  # 'default'

# setdefault - получить или установить значение по умолчанию
d = {'a': 1}
value = d.setdefault('b', 2)  # value = 2, d = {'a': 1, 'b': 2}
value = d.setdefault('a', 10) # value = 1 (существующее значение не перезаписывается)

# keys, values, items - view объекты
d = {'a': 1, 'b': 2, 'c': 3}
print(d.keys())               # dict_keys(['a', 'b', 'c'])
print(d.values())             # dict_values([1, 2, 3])
print(d.items())              # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Обход словаря
for key in d.keys():
    print(key)

for value in d.values():
    print(value)

for key, value in d.items():
    print(f"{key}: {value}")

# update - объединение словарей
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
d1.update(d2)                 # {'a': 1, 'b': 3, 'c': 4}
d1.update([('d', 5), ('e', 6)])  # из итератора
d1.update(x=7, y=8)           # из именованных аргументов

# pop - удаление с возвратом значения
d = {'a': 1, 'b': 2, 'c': 3}
value = d.pop('b')            # value = 2, d = {'a': 1, 'c': 3}
# value = d.pop('z')          # KeyError
value = d.pop('z', 'not found')  # 'not found'

# popitem - удаление последнего элемента (Python 3.7+)
d = {'a': 1, 'b': 2, 'c': 3}
key, value = d.popitem()      # key='c', value=3, d = {'a': 1, 'b': 2}
```

## Дополнительные методы (Python 3.9+)

```python
# Оператор | и |= для объединения словарей (Python 3.9+)
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = d1 | d2                   # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d1 |= d2                       # d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

## Полезные особенности:

```python
# Проверка существования ключа
if 'key' in d:
    print(d['key'])

# Генератор словарей (dictionary comprehension)
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Создание словаря из двух списков
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = dict(zip(keys, values))   # {'a': 1, 'b': 2, 'c': 3}

# Сортировка словаря
d = {'b': 2, 'a': 1, 'c': 3}
sorted_by_keys = dict(sorted(d.items()))        # {'a': 1, 'b': 2, 'c': 3}
sorted_by_values = dict(sorted(d.items(), key=lambda x: x[1]))  # {'a': 1, 'b': 2, 'c': 3}
```

## Важные замечания:
- Начиная с Python 3.7, словари сохраняют порядок вставки элементов
- Ключи должны быть хэшируемыми (обычно используются строки, числа, кортежи)
- `view` объекты (keys, values, items) динамически отражают изменения в словаре
- `popitem()` в версиях до 3.7 удалял произвольный элемент (не последний)