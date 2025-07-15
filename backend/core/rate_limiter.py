from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis
from config.settings import REDIS_URL


async def get_rate_limit_key(request):
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    return f"ratelimit:{token}"


@asynccontextmanager
async def lifespan(app):
    redis_client = redis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client, identifier=get_rate_limit_key)
    yield
