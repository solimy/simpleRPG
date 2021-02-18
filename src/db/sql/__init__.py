from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os


async def get_engine(_engine=None):
    if not _engine:
        _engine = create_async_engine(f'mysql+aiomysql://root@{os.environ["SQL_HOST"]}/db')
    return _engine

async def get_sql():
    engine = await get_engine()
    get_sql = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return get_sql()
