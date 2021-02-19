LOCK_EXPIRE = 10


LOCK = f'''
    redis.call("set", KEYS[1], 1)
    redis.call("expire", KEYS[1], {LOCK_EXPIRE})
    redis.call("del", KEYS[2])
'''


TRY_LOCK = f'''
    if redis.call("ttl", KEYS[1]) < 0 then
        {LOCK}
        return true
    else
        return false
    end
'''


RELEASE = f'''
    if redis.call("ttl", KEYS[1]) > 0 then
        redis.call("expire", KEYS[1], 0)
        if redis.call("llen", KEYS[2]) == 0 then
            redis.call("lpush", KEYS[2], 1)
        end
    end
'''


async def try_lock(redis, key, timeout=5, script=None):
    global LOCK_EXPIRE
    lock = f'{key}/lock'
    queue = f'{key}/lock/queue'
    if not script:
        script = await redis.script_load(TRY_LOCK)
    if await redis.evalsha(script, keys=[lock, queue]):
        return True
    else:
        if await redis.blpop(queue, timeout=timeout):
            await _lock(redis, lock, queue)
            return True
        else:
            return False


async def _lock(redis, lock, queue, script=None):
    global LOCK_EXPIRE
    if not script:
        script = await redis.script_load(LOCK)
    await redis.evalsha(script, keys=[lock, queue])


async def release(redis, key, script=None):
    lock = f'{key}/lock'
    queue = f'{key}/lock/queue'
    if not script:
        script = await redis.script_load(RELEASE)
    return await redis.evalsha(script, keys=[lock, queue])
