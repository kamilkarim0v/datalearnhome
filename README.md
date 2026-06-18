# T-Invest API to Postgres ETL Pipeline

## Описание
ETL-пайплайн для загрузки биржевых свечей из API T-Invest в PostgreSQL.

## Технологии
- Python (requests, pandas, sqlalchemy)
- PostgreSQL (Docker)
- API T-Invest

## Структура
- `app.py` — основной скрипт загрузки
- `docker-compose.yml` (взят отсюда https://github.com/finloop/airflow-postgres-superset-on-docker#)

## Как запустить
1. Создать .env с T_TOKEN
2. docker-compose up -d
3. python app.py

## Результат
Данные сохраняются в таблицу candles с инкрементальной загрузкой.