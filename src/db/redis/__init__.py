from aioredis import create_redis_pool
import os


async def get_redis(_pool=None):
    if not _pool:
        _pool = await create_redis_pool(os.environ['REDIS_HOST'])
    return _pool
