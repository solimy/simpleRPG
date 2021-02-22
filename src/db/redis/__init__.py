from aioredis import create_redis_pool
from loguru import logger
import asyncio
import atexit
import os


async def get_redis(_pool=None):
    if not _pool:
        _pool = await create_redis_pool(os.environ['REDIS_HOST'])
        logger.info('Redis pool created')
        @atexit.register
        def cleanup():
            _pool.close()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(_pool.wait_closed())
            logger.info('Redis pool cleaned-up')
    return _pool
