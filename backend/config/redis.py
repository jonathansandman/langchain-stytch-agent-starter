import redis.asyncio as redis
from config.settings import REDIS_URL


def redis_client() -> redis.Redis:
    if REDIS_URL:
        return redis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    raise ValueError("REDIS_URL environment variable is not set.")
