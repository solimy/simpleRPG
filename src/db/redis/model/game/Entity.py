from redis import Redis
import typing

from src.db.sql import model as sql_model


class Entity:
    redis: Redis
    id: bytes

    def __init__(self, redis: Redis, id: id):
        self.redis = redis
        self.id = id

    async def load(self, entity: sql_model.Entity) -> str:
        pass

    async def get_alias(self) -> str:
        return await self.redis.get(b'/entity/%b/alias' % self.id)

    async def set_alias(self, value: str):
        await self.redis.set(b'/entity/%b/alias' % self.id, value)
