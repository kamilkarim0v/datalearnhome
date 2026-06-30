# src_main/api_job_logger.py
import json
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

class ApiJobLogger:
    def __init__(self, db_manager):
        self.db = db_manager

    def save_job(self, endpoint, request_payload, response_data, status_code):
        """
        Сохраняет информацию об API-запросе в таблицу raw.extract_api_jobs.
        metadata: словарь с полями figi, interval, from_dt, to_dt (для быстрой фильтрации)
        """

        # Преобразуем в JSON-строки
        request_json = json.dumps(request_payload, default=str)  # default=str для datetime
        response_json = json.dumps(response_data, default=str)

        sql = """
            INSERT INTO raw.extract_api_jobs
            (endpoint, request_payload, response_data, status_code)
            VALUES (:endpoint, :request_payload, :response_data, :status_code)
        """
        params = {
            "endpoint": endpoint,
            "request_payload": request_json,
            "response_data": response_json,
            "status_code": status_code,
        }

        with self.db.engine.begin() as conn:
            conn.execute(text(sql), params)
        logger.info(f"API job logged: {endpoint} (status {status_code})")