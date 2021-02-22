from redis import Redis
import typing


from src.db.redis.model import Item


class Inventory:
    redis: Redis
    id: bytes
    items: typing.List[Item]

    def __init__(self, redis: Redis, id: id):
        self.redis = redis
        self.id = id
