import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BaseClient:
    """Клиент для работы с API T-Invest."""

    def __init__(self):
        """Инициализация: берём токен из переменных окружения."""
        self.token = os.getenv('T_TOKEN')
        if not self.token:
            raise ValueError("T_TOKEN не задан в .env файле")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.base_url = 'https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1'

    def _post(self, endpoint:str, payload:dict) -> dict:
        """Отправляем POST-запрос к API."""
        url = f'{self.base_url}/{endpoint}'
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            logger.error(f'Ошибка при запросе {response.url}')
            raise Exception(response.text)