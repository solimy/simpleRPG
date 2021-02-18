from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
import asyncio


from src.db.sql import get_engine
import src.db.sql.model as models


async def main():
    engine = await get_engine()
    async with engine.begin() as conn:
        for model in dir(models):
            _model = getattr(models, model)
            is_table = type(_model) == type(declarative_base())
            if is_table:
                await conn.run_sync(_model.metadata.drop_all)
                logger.info(f'Table "{model}" deleted')
                await conn.run_sync(_model.metadata.create_all)
                logger.info(f'Table "{model}" created')


if __name__ == "__main__":
    asyncio.run(main())
    logger.info('All tables created')
