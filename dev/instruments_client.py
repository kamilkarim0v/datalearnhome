from .base_client import BaseClient

class InstrumentsClient(BaseClient):
    def get_assets(self, instrument_type="stock"):
        payload = {"instrumentType": instrument_type}
        return self._post("InstrumentsService/GetTradableAssets", payload)