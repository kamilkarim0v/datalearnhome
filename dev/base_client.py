import os
import requests
import logging

class BaseClient:
    def __init__(self):
        self.token = os.getenv('T_TOKEN')
        if not self.token:
            raise ValueError("Token is empty")
        self.base_url = 'https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def _post(self, endpoint:str, payload:dict) -> dict:
        url = f'{self.base_url}/{endpoint}'
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            
