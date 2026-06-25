# Используем официальный легкий образ Python
FROM python:3.11-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем dbt-core и адаптер для PostgreSQL
RUN pip install --no-cache-dir dbt-core dbt-postgres

# Создаем рабочую директорию для dbt проекта
WORKDIR /usr/app/dbt

# Копируем файлы dbt проекта внутрь контейнера
COPY ./dbt /usr/app/dbt

# Точка входа: всегда запускаем dbt
ENTRYPOINT ["dbt"]