from redis import Redis


class Item:
    redis: Redis
    id: bytes

    def __init__(self, redis: Redis, id: id):
        self.redis = redis
        self.id = id
