from app.database.database import AsyncSessionLocal
from app.database.redis import pool
import redis.asyncio as redis


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_redis():
    return redis.Redis(connection_pool=pool)
