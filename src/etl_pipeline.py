import logging
import pandas as pd
from datetime import datetime, timedelta, timezone
from src.api_client import TInvestClient
from src.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class CandlesETL:
    """ETL-пайплайн для загрузки свечей."""

    def __init__(self, figi: str, interval: str, days_back: int = 1):
        self.figi = figi
        self.interval = interval
        self.days_back = days_back
        self.client = TInvestClient()
        self.db = DatabaseManager()
        self.df = None

    def extract(self):
        """Извлекает данные из API."""
        to_dt = datetime.now(timezone.utc)
        from_dt = to_dt - timedelta(days=self.days_back)
        raw_data = self.client.get_candles(self.figi, from_dt, to_dt, self.interval)
        # Преобразуем в DataFrame с помощью json_normalize
        df = pd.json_normalize(raw_data['candles'], sep='_')
        # Переименовываем столбцы из CamelCase в snake_case
        import re
        def camel_to_snake(name):
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
            return name.lower()
        df.columns = [camel_to_snake(col) for col in df.columns]
        # Преобразуем наносекунды в десятичные числа
        for col in ['open', 'close', 'high', 'low']:
            df[col] = df[f'{col}_units'].astype(float) + df[f'{col}_nano'] / 1e9
        # Добавляем служебные столбцы
        df['interval'] = self.interval
        df['figi'] = self.figi
        self.df = df
        logger.info(f"Извлечено {len(df)} свечей")
        return df

    def transform(self):
        """Трансформации (пока ничего не делаем, но оставляем место для будущего)."""
        # Можно добавить фильтрацию, вычисления и т.д.
        pass

    def load(self):
        """Загружает данные в БД."""
        if self.df is None or self.df.empty:
            logger.warning("Нет данных для загрузки")
            return
        # Создаём основную и временную таблицы
        self.db.create_candles_table()
        self.db.create_temp_table()
        # Загружаем во временную
        self.db.insert_temp_table(self.df)
        # Мержим в основную
        self.db.merge_temp_to_main()
        # Проверяем дубликаты
        self.db.check_duplicates()
        # Выводим общее количество
        total = self.db.get_total_count()
        logger.info(f"Общее количество свечей в БД: {total}")

    def run(self):
        """Запускает весь пайплайн."""
        self.extract()
        self.transform()
        self.load()
        self.db.close()
        logger.info("ETL пайплайн завершён успешно")