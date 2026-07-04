from datetime import datetime
import logging
from .api_client import BaseClient

logger = logging.getLogger(__name__)

class InstrumentService(BaseClient):
    def __init__(self):
        super().__init__()
        self.endpoint_base = 'InstrumentsService'

    def get_assets(self, instrument_type: str = 'share', instrument_status: str = 'all') -> tuple[dict, int, str, dict]:
        """
        Получение списка активов по типу и статусу
        """

        endpoint = f"{self.endpoint_base}/GetAssets"

        instrument_type_map = {
            "share": "INSTRUMENT_TYPE_SHARE",
            "bond": "INSTRUMENT_TYPE_BOND",
            "currency": "INSTRUMENT_TYPE_CURRENCY",
            "futures": "INSTRUMENT_TYPE_FUTURES",
            "option": "INSTRUMENT_TYPE_OPTION",
            "etf": "INSTRUMENT_TYPE_ETF", 
            "sp": "INSTRUMENT_TYPE_SP", 
            "clearing_certificate": "IINSTRUMENT_TYPE_CLEARING_CERTIFICATE", 
            "index": "IINSTRUMENT_TYPE_INDEX", 
            "commodity": "IINSTRUMENT_TYPE_COMMODITY", 
            "dfa": "IINSTRUMENT_TYPE_DFA",
            "unspecified": "INSTRUMENT_TYPE_UNSPECIFIED"            
        }

        instrument_status_map = {
            "all": "INSTRUMENT_STATUS_ALL",
            "base": "INSTRUMENT_STATUS_BASE",
            "unspecified": "INSTRUMENT_STATUS_UNSPECIFIED"
        }

        payload = {
            "instrumentType": instrument_type_map[instrument_type],
            "instrumentStatus": instrument_status_map[instrument_status]
        }

        logger.info(f"Запрос к {endpoint}: {instrument_type = }, {instrument_status = }")

        response, status_code = self._post(endpoint, payload)

        return response, status_code, endpoint, payload