from sqlalchemy import create_engine
from loguru import logger
import os


from src.db.sql.model import Base


if __name__ == "__main__":
    logger.info('DB initialization')
    engine = create_engine(f'mysql+pymysql://root@{os.environ["SQL_HOST"]}')
    try:
        engine.execute('drop database db')
    except: pass
    engine.execute('create database db')
    engine = create_engine(f'mysql+pymysql://root@{os.environ["SQL_HOST"]}/db')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info('DB initialized')
