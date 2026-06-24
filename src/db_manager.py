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
        # self.engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{db}')
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{db}')
        # self.connection = self.engine.connect()

    def create_candles_table(self):
        """Создаёт таблицу candles, если её нет."""
        sql = '''
            CREATE TABLE IF NOT EXISTS candles (
                time TIMESTAMPTZ,
                figi VARCHAR(255),
                interval VARCHAR(255),
                open DECIMAL(12,2),
                close DECIMAL(12,2),
                high DECIMAL(12,2),
                low DECIMAL(12,2),
                is_complete BOOLEAN,
                candle_source VARCHAR(255),
                volume BIGINT,
                volume_buy BIGINT,
                volume_sell BIGINT,
                open_units BIGINT,
                open_nano BIGINT,
                close_units BIGINT,
                close_nano BIGINT,
                high_units BIGINT,
                high_nano BIGINT,
                low_units BIGINT,
                low_nano BIGINT,
                PRIMARY KEY (time, figi, interval)
            )
        '''

        with self.engine.begin() as conn:
            conn.execute(text(sql))

        logger.info("Таблица candles создана или уже существует")

    def create_temp_table(self):
        """Создаёт временную таблицу temp_candles."""
        sql = '''
            DROP TABLE IF EXISTS temp_candles;
            CREATE TABLE temp_candles (
                time TIMESTAMPTZ,
                figi VARCHAR(255),
                interval VARCHAR(255),
                open DECIMAL(12,2),
                close DECIMAL(12,2),
                high DECIMAL(12,2),
                low DECIMAL(12,2),
                is_complete BOOLEAN,
                candle_source VARCHAR(255),
                volume BIGINT,
                volume_buy BIGINT,
                volume_sell BIGINT,
                open_units BIGINT,
                open_nano BIGINT,
                close_units BIGINT,
                close_nano BIGINT,
                high_units BIGINT,
                high_nano BIGINT,
                low_units BIGINT,
                low_nano BIGINT,
                PRIMARY KEY (time, figi, interval)
            )
        '''
        with self.engine.begin() as conn:
            conn.execute(text(sql))
        logger.info("Временная таблица создана")

    def insert_temp_table(self, df: pd.DataFrame):
        """Вставляет DataFrame в temp_candles."""
        # Удаляем дубликаты (был случай, когда API выдало несколько строк с одинаковыми параметрами)
        duplicates_before = len(df)
        df = df.drop_duplicates(subset=['time', 'figi', 'interval'], keep='first')
        duplicates_after = len(df)
        if duplicates_before != duplicates_after:
            logger.warning(f"Удалено {duplicates_before - duplicates_after} дубликатов во временной таблице")

        df.to_sql('temp_candles', self.engine, if_exists='append', index=False, method='multi')
        logger.info(f"Загружено {duplicates_after} строк в temp_candles")

    def merge_temp_to_main(self):
        """Инкрементальная загрузка из temp в основную таблицу."""
        sql = '''
            DELETE FROM candles
            WHERE (time, figi, interval) IN (
                SELECT time, figi, interval FROM temp_candles
            );
            INSERT INTO candles
            SELECT * FROM temp_candles;
        '''
        with self.engine.begin() as conn:
            conn.execute(text(sql))
        logger.info("Инкрементальная загрузка завершена")

    def check_duplicates(self) -> bool:
        """Проверяет наличие дубликатов в основной таблице."""
        sql = '''
            SELECT figi, interval, time, COUNT(*) as cnt_rows
            FROM candles
            GROUP BY figi, interval, time
            HAVING COUNT(*) > 1
        '''
        df = pd.read_sql(sql, self.engine)
        if df.empty:
            logger.info("Дубликатов нет")
            return True
        else:
            logger.error("Обнаружены дубликаты:")
            logger.error(df.to_string())
            return False

    def get_total_count(self) -> int:
        """Возвращает общее количество записей в таблице candles."""
        sql = "SELECT COUNT(*) FROM candles"
        df = pd.read_sql(sql, self.engine)
        return df.iloc[0, 0]

    # def close(self):
    #     """Закрывает соединение с БД."""
    #     self.connection.close()
    #     logger.info("Соединение с БД закрыто")