# Базовые типы данных Python и их методы

## 1. Числовые типы

### int (целые числа)
```python
# Методы int (на самом деле их немного, большинство - операторы)
num = 42

# Преобразования
num.bit_length()        # количество бит для представления (2)
num.to_bytes(2, 'big')  # в байты (b'\x00*')
int.from_bytes(b'\x00*', 'big')  # из байт в int

# Проверки
num.is_integer()        # True (для int всегда True, полезно для float)
```

### float (числа с плавающей точкой)
```python
f = 3.14

f.is_integer()          # проверка, целое ли число (False)
f.as_integer_ratio()    # как дробь (3537115881217719/1125899906842624)
f.hex()                 # в шестнадцатеричное представление
float.fromhex('0x1.91eb851eb851fp+1')  # из hex в float
```

### complex (комплексные числа)
```python
c = 3 + 4j

c.real                  # действительная часть (3.0)
c.imag                  # мнимая часть (4.0)
c.conjugate()           # сопряженное число (3-4j)
```

## 2. str (строки)

### Основные методы
```python
s = "Hello World"

# Преобразование регистра
s.upper()               # "HELLO WORLD"
s.lower()               # "hello world"
s.capitalize()          # "Hello world"
s.title()               # "Hello World"
s.swapcase()            # "hELLO wORLD"
s.casefold()            # для сравнения без учета регистра

# Поиск и замена
s.count('l')            # 3
s.find('l')             # 2 (первое вхождение, -1 если нет)
s.rfind('l')            # 9 (последнее вхождение)
s.index('l')            # 2 (как find, но вызывает ValueError)
s.replace('World', 'Python')  # "Hello Python"
s.startswith('He')      # True
s.endswith('ld')        # True

# Проверка содержимого
s.isalpha()             # False (есть пробел)
s.isdigit()             # False
s.isalnum()             # False
s.isspace()             # False
s.islower()             # False
s.isupper()             # False
s.istitle()             # True (каждое слово с заглавной)

# Разделение и объединение
s.split()               # ['Hello', 'World']
s.split('l')            # ['He', '', 'o Wor', 'd']
s.rsplit('l', 1)        # ['Hello Wor', 'd']
s.partition(' ')        # ('Hello', ' ', 'World')
'-'.join(['a', 'b', 'c'])  # "a-b-c"

# Удаление пробелов
"  hello  ".strip()     # "hello"
"  hello  ".lstrip()    # "hello  "
"  hello  ".rstrip()    # "  hello"
"hello".strip('ho')     # "ell"

# Выравнивание
s.center(20, '*')       # "****Hello World*****"
s.ljust(20, '-')        # "Hello World--------"
s.rjust(20, '-')        # "--------Hello World"
s.zfill(20)             # "000000000Hello World"

# Форматирование
name = "Alice"
age = 30
f"{name} is {age}"      # f-строки
"{} is {}".format(name, age)
"{name} is {age}".format(name=name, age=age)

# Кодирование
s.encode('utf-8')       # b'Hello World'
```

## 3. list (списки)

```python
lst = [1, 2, 3, 4, 5]

# Добавление элементов
lst.append(6)           # [1,2,3,4,5,6]
lst.insert(2, 99)       # [1,2,99,3,4,5,6]
lst.extend([7,8])       # [1,2,99,3,4,5,6,7,8]

# Удаление элементов
lst.remove(99)          # удаляет первое вхождение 99
lst.pop()               # удаляет и возвращает последний (8)
lst.pop(2)              # удаляет и возвращает элемент по индексу
lst.clear()             # очищает список

# Информация о списке
lst = [1,2,3,2,4,2]
lst.index(2)            # 1 (первое вхождение)
lst.count(2)            # 3
len(lst)                # длина списка

# Сортировка и обратный порядок
lst.sort()              # сортировка на месте
lst.sort(reverse=True)  # по убыванию
lst.reverse()           # обратный порядок
sorted(lst)             # возвращает новый отсортированный список

# Копирование
lst2 = lst.copy()       # поверхностная копия
lst2 = lst[:]           # тоже копия

# Другие методы
lst = [1, 2, 3]
max(lst), min(lst), sum(lst)  # 3, 1, 6
any([False, True, False])     # True
all([True, True, True])       # True
```

## 4. tuple (кортежи)

Кортежи неизменяемы, поэтому методов мало:

```python
t = (1, 2, 3, 2, 4)

t.count(2)              # 2 (сколько раз встречается)
t.index(3)              # 2 (индекс первого вхождения)
len(t)                  # длина

# Преобразования
list(t)                 # в список
tuple([1,2,3])          # в кортеж из списка
```

## 5. dict (словари)

```python
d = {'a': 1, 'b': 2, 'c': 3}

# Доступ и изменение
d.get('a')              # 1 (без ошибки если нет ключа)
d.get('z', 'default')   # 'default'
d.setdefault('d', 4)    # устанавливает если нет ключа
d.update({'e': 5})      # обновление
d.keys()                # view объектов ключей
d.values()              # view значений
d.items()               # view пар (ключ, значение)

# Удаление
d.pop('a')              # удаляет и возвращает значение
d.popitem()             # удаляет последнюю добавленную пару
d.clear()               # очищает

# Копирование
d2 = d.copy()
d2 = dict(d)            # тоже копия

# Создание
dict.fromkeys(['x','y'], 0)  # {'x': 0, 'y': 0}
```

## 6. set (множества) и frozenset

```python
s = {1, 2, 3}

# Добавление/удаление
s.add(4)                # {1,2,3,4}
s.remove(4)             # удаляет (KeyError если нет)
s.discard(5)            # удаляет без ошибки
s.pop()                 # удаляет произвольный элемент
s.clear()               # очищает

# Операции
s1 = {1, 2, 3}
s2 = {3, 4, 5}
s1.union(s2)            # {1,2,3,4,5}
s1.intersection(s2)     # {3}
s1.difference(s2)       # {1,2}
s1.symmetric_difference(s2)  # {1,2,4,5}

# Проверки
s1.issubset(s2)         # False
s1.issuperset({1,2})    # True
s1.isdisjoint({4,5})    # True

# Обновления на месте
s1.update(s2)           # добавляет элементы
s1.intersection_update(s2)  # оставляет только общие
s1.difference_update(s2)    # удаляет элементы из s2
s1.symmetric_difference_update(s2)

# frozenset - неизменяемая версия
fs = frozenset([1,2,3])
# fs.add(4) - TypeError!
```

## 7. bool (булевы значения)

```python
# Булевы значения - подкласс int
True + True == 2        # True
bool(0)                 # False
bool(42)                # True
bool('')                # False
bool('hello')           # True
bool([])                # False
bool([1,2])             # True

# Методы (почти нет, кроме преобразований)
str(True)               # "True"
int(True)               # 1
int(False)              # 0
```

## 8. bytes и bytearray

```python
# bytes (неизменяемый)
b = b'hello'
b.hex()                 # '68656c6c6f'
b.upper()               # b'HELLO'
b.find(b'l')            # 2

# bytearray (изменяемый)
ba = bytearray(b'hello')
ba.append(33)           # b'hello!'
ba.extend(b' world')    # b'hello! world'
ba.replace(b'l', b'L')  # b'heLLo! worLd'
```

## Общие встроенные функции для всех типов

```python
type(obj)               # тип объекта
id(obj)                 # уникальный идентификатор
isinstance(obj, type)   # проверка типа
len(obj)                # длина (для коллекций)
str(obj)                # строковое представление
repr(obj)               # "официальное" представление
hash(obj)               # хэш-значение (для неизменяемых)
```

## Особенности и нюансы

1. **Изменяемые типы**: list, dict, set, bytearray
2. **Неизменяемые**: int, float, str, tuple, frozenset, bytes
3. **Все методы возвращают новые объекты для неизменяемых типов**
4. **Методы изменяемых типов часто модифицируют объект на месте и возвращают None**