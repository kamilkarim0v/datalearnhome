from .base_client import BaseClient

class MarketDataClient(BaseClient):
    def get_candles(self, figi, from_dt, to_dt, interval):
        intervals = {...}
        payload = {...}
        return self._post("MarketDataService/GetCandles", payload)