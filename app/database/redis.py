import redis.asyncio as redis

from app.settings import settings


def create_redis_pool():
    return redis.ConnectionPool(
        host=settings().redis_url,
        port=settings().redis_port,
        db=0,
        decode_responses=True,
    )


pool = create_redis_pool()
