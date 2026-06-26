import os
import requests
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class TInvestClient:
    """Клиент для работы с API T-Invest."""

    def __init__(self):
        """Инициализация: берём токен из переменных окружения."""
        self.token = os.getenv('T_TOKEN')
        if not self.token:
            raise ValueError("T_TOKEN не задан в .env файле")
        self.base_url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_candles(self, figi: str, from_dt: datetime, to_dt: datetime, interval: str) -> dict:
        """
        Запрашивает свечи по figi за указанный период.
        interval: '1min', '5min', '15min', 'hour', 'day'
        Возвращает JSON-ответ от API.
        """
        intervals_map = {
            "1min": "CANDLE_INTERVAL_1_MIN",
            "5min": "CANDLE_INTERVAL_5_MIN",
            "15min": "CANDLE_INTERVAL_15_MIN",
            "hour": "CANDLE_INTERVAL_HOUR",
            "day": "CANDLE_INTERVAL_DAY",
            "2min": "CANDLE_INTERVAL_2_MIN",
            "3min": "CANDLE_INTERVAL_3_MIN",
            "10min": "CANDLE_INTERVAL_10_MIN",
            "30min": "CANDLE_INTERVAL_30_MIN",
            "2hour": "CANDLE_INTERVAL_2_HOUR",
            "4hour": "CANDLE_INTERVAL_4_HOUR",
            "week": "CANDLE_INTERVAL_WEEK",
            "month": "CANDLE_INTERVAL_MONTH",
            "5sec": "CANDLE_INTERVAL_5_SEC",
            "10sec": "CANDLE_INTERVAL_10_SEC",
            "30sec": "CANDLE_INTERVAL_30_SEC"
        }
        payload = {
            "figi": figi,
            "from": from_dt.isoformat(),
            "to": to_dt.isoformat(),
            "interval": intervals_map[interval]
        }
        logger.info(f"Запрос к API: figi={figi}, interval={interval}, from={from_dt}")
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code == 200:
            logger.info(f"Успешно получены данные")
            return response.json()
        else:
            logger.error(f"Ошибка API: {response.status_code} - {response.text}")
            response.raise_for_status()  # вызовет исключение при ошибке