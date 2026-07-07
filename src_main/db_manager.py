import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Менеджер для работы с PostgreSQL."""

    def __init__(self):
        """Создаём подключение к БД на основе переменных окружения."""
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        db = os.getenv('POSTGRES_DB')
        host = os.getenv('POSTGRES_HOST', 'localhost')
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{db}')

    def create_table(self, table_name, columns_type, primary_key = None):
        """
        Создание таблицы в базе данных.
        """
        
        cols_def = ', '.join([f'{col} {typ}' for col, typ in columns_type.items()])
        pk_def = f', PRIMARY KEY ({primary_key})' if primary_key else ''
        sql = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {cols_def}
                {pk_def}
            );
        '''

        with self.engine.begin() as conn:
            conn.execute(text(sql))
        logger.info(f"Таблица {table_name} создана")

    def create_schema(self, schema_name):
        """
        Создание схемы в базе данных.
        """
        sql = f'CREATE SCHEMA IF NOT EXISTS {schema_name}'

        with self.engine.begin() as conn:
            conn.execute(text(sql))
        logger.info(f"Схема {schema_name} создана")


    def insert_data(self, table_name, data):
        """
        Вставка данных в таблицу.
        """
        pass


    def create_table_from_df(self, df, table_name, columns_type = None, primary_key = None):
        """
        Создание таблицы в базе данных из датафрейма.
        :param df: Датафрейм с данными для создания таблицы.
        :param table_name: Название таблицы.
        :param columns_type: Список столбцов и их типов данных.
        :param primary_key: Название столбца с первичным ключом.
        """
        pass

    def insert_data_from_df(self, df, table_name):
        """
        Вставка данных из датафрейма в таблицу.
        :param df: Датафрейм с данными для вставки.
        :param table_name: Название таблицы.
        """
        pass
    
    def delete_data_from_db(self, df, table_name):
        """
        Удаление данных из таблицы.
        :param df: Датафрейм с данными для удаления.
        :param table_name: Название таблицы.
        """
        pass

    def merge_temp_to_main(self, temp_table, main_table):
        """
        Инкрементальная загрузка данных из временной таблицы в основную таблицу.
        :param temp_table: Название временной таблицы.
        :param main_table: Название основной таблицы.
        """
        pass