# Работа с циклами в Python

## 1. Цикл `for`

### Базовый синтаксис
```python
# Итерация по последовательности
for элемент in последовательность:
    # тело цикла
```

### Примеры с разными типами данных

```python
# Строка
for char in "Hello":
    print(char)  # H, e, l, l, o

# Список
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Кортеж
for num in (1, 2, 3):
    print(num)

# Словарь
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:           # итерация по ключам
    print(key, d[key])

for value in d.values():    # по значениям
    print(value)

for key, value in d.items(): # по парам
    print(f"{key}: {value}")

# Множество
for item in {1, 2, 3}:
    print(item)
```

### Функция `range()`

```python
# range(stop) - от 0 до stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - от start до stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step) - с шагом
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Обратный порядок
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### Функция `enumerate()` - получение индекса и значения

```python
fruits = ['apple', 'banana', 'cherry']

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# С указанием начального индекса
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")
```

### Функция `zip()` - параллельная итерация

```python
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['NYC', 'LA', 'Chicago']

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} from {city}")

# Для списков разной длины - обрезается по короткому
for a, b in zip([1,2,3], ['a','b']):
    print(a, b)  # (1,'a'), (2,'b')

# zip_longest из itertools для заполнения
from itertools import zip_longest
for a, b in zip_longest([1,2,3], ['a','b'], fillvalue='None'):
    print(a, b)  # (1,'a'), (2,'b'), (3,'None')
```

## 2. Цикл `while`

### Базовый синтаксис
```python
while условие:
    # тело цикла
    # важно: условие должно стать False
```

### Примеры
```python
# Счетчик
i = 0
while i < 5:
    print(i)
    i += 1

# Бесконечный цикл с break
while True:
    user_input = input("Введите 'quit' для выхода: ")
    if user_input == 'quit':
        break
    print(f"Вы ввели: {user_input}")

# Ожидание условия
import random
target = random.randint(1, 10)
guess = 0
while guess != target:
    guess = int(input("Угадайте число: "))
    if guess < target:
        print("Больше!")
    elif guess > target:
        print("Меньше!")
print("Угадали!")
```

## 3. Управление циклами

### `break` - досрочный выход
```python
# Поиск первого четного числа
numbers = [1, 3, 5, 8, 10, 11]
for num in numbers:
    if num % 2 == 0:
        print(f"Первое четное: {num}")
        break  # выход из цикла
```

### `continue` - переход к следующей итерации
```python
# Пропуск четных чисел
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # только нечетные: 1,3,5,7,9
```

### `else` в циклах - выполняется, если не было break
```python
# Поиск элемента
numbers = [1, 2, 3, 4, 5]
search = 6

for num in numbers:
    if num == search:
        print(f"Нашли {search}!")
        break
else:
    print(f"{search} не найден")  # выполнится, т.к. break не было

# Пример с while
count = 0
while count < 3:
    print(f"Попытка {count + 1}")
    count += 1
else:
    print("Цикл завершен без break")
```

## 4. Вложенные циклы

```python
# Таблица умножения
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} × {j} = {i*j}")
    print("---")

# Поиск дубликатов
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for element in row:
        print(element, end=' ')
    print()

# break во вложенных циклах
for i in range(3):
    for j in range(3):
        if i == j == 1:
            break  # break только внутренний цикл
        print(f"({i},{j})")
```

## 5. Генераторы списков (list comprehensions)

```python
# Классический цикл
squares = []
for x in range(10):
    squares.append(x**2)

# Генератор списка (более Pythonic)
squares = [x**2 for x in range(10)]

# С условием
evens = [x for x in range(10) if x % 2 == 0]

# Вложенные генераторы
pairs = [(x, y) for x in range(3) for y in range(3)]

# Генераторы словарей и множеств
square_dict = {x: x**2 for x in range(5)}
even_set = {x for x in range(10) if x % 2 == 0}
```

## 6. Генераторы (yield) - ленивые вычисления

```python
def count_up_to(n):
    i = 0
    while i < n:
        yield i  # возвращает значение и "замораживает" функцию
        i += 1

for num in count_up_to(5):
    print(num)  # 0,1,2,3,4

# Генераторные выражения
sum_of_squares = sum(x**2 for x in range(100))  # без создания списка
```

## 7. Полезные паттерны и идиомы

### Итерация по двум спискам одновременно
```python
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']

for i, (a, b) in enumerate(zip(list1, list2)):
    print(f"{i}: {a} -> {b}")
```

### Получение соседних элементов
```python
items = [1, 2, 3, 4, 5]
for prev, curr in zip(items, items[1:]):
    print(f"{prev} -> {curr}")
```

### Итерация по срезам
```python
for chunk in zip(*[iter(range(10))]*3):
    print(chunk)  # (0,1,2), (3,4,5), (6,7,8)
```

### Прогресс-бар с enumerate
```python
items = range(100)
total = len(items)
for i, item in enumerate(items):
    if i % 10 == 0:
        print(f"Прогресс: {i/total*100:.0f}%")
```

## 8. Оптимизация и производительность

### Используйте локальные переменные
```python
# Медленно
for i in range(1000000):
    len(my_list)  # глобальный поиск

# Быстро
list_len = len  # локальная переменная
for i in range(1000000):
    list_len(my_list)
```

### Избегайте range(len()) при итерации
```python
# Плохо
for i in range(len(items)):
    print(items[i])

# Хорошо
for item in items:
    print(item)

# Если нужен индекс
for i, item in enumerate(items):
    print(i, item)
```

### Используйте генераторы для больших данных
```python
# Создает огромный список (плохо)
sum([x**2 for x in range(10000000)])

# Использует генератор (хорошо)
sum(x**2 for x in range(10000000))
```

## 9. Бесконечные циклы и их остановка

```python
# Использование таймаута
import time
start = time.time()
timeout = 5

while time.time() - start < timeout:
    # делаем что-то
    pass

# Счетчик попыток
attempts = 0
max_attempts = 3
while attempts < max_attempts:
    # пробуем операцию
    attempts += 1
```

## 10. Примеры из реальной практики

### Обработка файла построчно
```python
with open('file.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:  # пропуск пустых строк
            continue
        if line.startswith('#'):  # комментарии
            continue
        # обработка строки
        print(line)
```

### Пагинация через API
```python
def fetch_all_pages(base_url):
    page = 1
    while True:
        response = api_call(f"{base_url}?page={page}")
        if not response['data']:
            break
        for item in response['data']:
            yield item
        page += 1
```

### Перебор комбинаций
```python
from itertools import product, permutations, combinations

# Декартово произведение
for a, b in product([1,2], ['a','b']):
    print(a, b)

# Перестановки
for perm in permutations([1,2,3], 2):
    print(perm)

# Сочетания
for combo in combinations([1,2,3,4], 3):
    print(combo)
```

## Важные советы

1. **Не изменяйте список во время итерации по нему** - используйте копию или итерируйте в обратном порядке
2. **for лучше while для итерации по коллекциям**
3. **while лучше для бесконечных циклов и сложных условий**
4. **Используйте else в циклах** для обработки случая "не найдено"
5. **Генераторы списков часто быстрее** явных циклов для создания коллекций
6. **break выходит только из самого внутреннего цикла**