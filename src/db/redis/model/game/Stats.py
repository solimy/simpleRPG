from redis import Redis


class Stats:
    redis: Redis
    id: bytes
    health: int

    def __init__(self, redis: Redis, id: id):
        self.redis = redis
        self.id = id
