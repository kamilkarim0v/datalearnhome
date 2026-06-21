import sys
import os
import argparse
import logging

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.etl_pipeline import CandlesETL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Загрузка свечей из T-Invest API в PostgreSQL")
    parser.add_argument('--figi', default='BBG004730N88', help='FIGI инструмента')
    parser.add_argument('--interval', default='15min', choices=['1min', '5min', '15min', 'hour', 'day'])
    parser.add_argument('--days', type=int, default=1, help='За сколько дней загрузить')
    args = parser.parse_args()

    logger.info(f"Запуск ETL с параметрами: figi={args.figi}, interval={args.interval}, days={args.days}")
    etl = CandlesETL(args.figi, args.interval, args.days)
    etl.run()

if __name__ == "__main__":
    main()