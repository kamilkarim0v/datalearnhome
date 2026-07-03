from datetime import datetime
import logging
from .api_client import BaseClient

logger = logging.getLogger(__name__)

class MarketDataService(BaseClient):

    def __init__(self):
        super().__init__()
        self.endpoint = "MarketDataService/GetCandles"

    def get_candles(self, figi: str, from_dt: datetime, to_dt: datetime, interval: str) -> tuple[dict, str, str, dict]:

        
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
        
        response, status_code = self._post(self.endpoint, payload)

        return response, status_code, self.endpoint, payload
