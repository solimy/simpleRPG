from loguru import logger
import time
import os


from src.db.redis import client as redis


if __name__ == 'main':
    while True:
        time.sleep(os.environ['SAVE_INTERVAL_SECONDS'])