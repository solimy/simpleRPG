from redis import Redis


class Position:
    redis: Redis
    id: bytes
    location: str
    x: int
    y: int
    z: int

    def __init__(self, redis: Redis, id: id):
        self.redis = redis
        self.id = id

    async def get_location(self) -> str:
        return await self.redis.get(b'/entity/%b/location' % self.id)

    async def set_location(self, value: str):
        await self.redis.set(b'/entity/%b/location' % self.id, value)

    async def get_x(self) -> int:
        return await self.redis.get(b'/entity/%b/x' % self.id)

    async def set_x(self, value: int):
        await self.redis.set(b'/entity/%b/x' % self.id, value)

    async def get_y(self) -> int:
        return await self.redis.get(b'/entity/%b/y' % self.id)

    async def set_y(self, value: int):
        await self.redis.set(b'/entity/%b/y' % self.id, value)

    async def get_z(self) -> int:
        return await self.redis.get(b'/entity/%b/z' % self.id)

    async def set_z(self, value: int):
        await self.redis.set(b'/entity/%b/z' % self.id, value)
