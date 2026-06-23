## 1. Виртуальное окружение (venv)

### Создание
```bash
# В папке проекта
python -m venv venv

# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

### Активация
```bash
# Windows (cmd)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### Проверка активации
```bash
# Должен быть (venv) в начале строки
which python  # покажет путь внутри venv

# Установка пакета
pip install requests

# Просмотр установленных
pip list

# Деактивация
deactivate
```

### Файл зависимостей
```bash
# Сохранить все текущие пакеты
pip freeze > requirements.txt

# Установить из файла
pip install -r requirements.txt
```

## 2. Секретные токены

### Плохой способ ❌
```python
# config.py
TOKEN = "sk-12345"  # Никогда так не делай!
```

### Хороший способ ✅ (python-dotenv)

```bash
# Установка
pip install python-dotenv
```

**Создай файл `.env` в корне проекта:**
```env
API_TOKEN=sk_real_secret_token_12345
DATABASE_URL=postgresql://localhost/mydb
DEBUG=False
```

**Файл `.gitignore` (обязательно):**
```
.env
venv/
__pycache__/
```

**Использование в коде:**
```python
from dotenv import load_dotenv
import os

# Загружаем .env в переменные окружения
load_dotenv()

# Читаем токены
token = os.getenv("API_TOKEN")
db_url = os.getenv("DATABASE_URL")
debug = os.getenv("DEBUG", "False")  # значение по умолчанию

print(f"Token: {token}")  # для проверки
```

### Пример с реальным API
```python
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# response = requests.post(url, headers=headers, json=data)
```

## 3. Полный рабочий процесс

```bash
# 1. Создать проект
mkdir my_project
cd my_project

# 2. Создать окружение
python -m venv venv

# 3. Активировать
source venv/bin/activate  # или для Windows: venv\Scripts\activate

# 4. Установить пакеты
pip install python-dotenv requests

# 5. Сохранить зависимости
pip freeze > requirements.txt

# 6. Создать .env и добавить в .gitignore
echo "SECRET_TOKEN=abc123" > .env
echo ".env" >> .gitignore
echo "venv/" >> .gitignore

# 7. Написать код (main.py)
```

**main.py:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("SECRET_TOKEN")
print(f"Working with token: {TOKEN[:5]}...")  # показываем только начало
```

```bash
# 8. Запустить
python main.py
```

## Главные правила:
1. **Всегда** создавай venv для каждого проекта
2. **Никогда** не коммить `.env` и `venv/` в git
3. **Всегда** добавляй `.env` в `.gitignore`
4. **Сохраняй** `requirements.txt`

Готово! Ты в безопасности.