import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from contextlib import asynccontextmanager
import redis.asyncio as redis
from agent import explain_like_im_five
from auth import (
    get_current_user_and_organization,
    can_user_create_topic,
    can_user_read_topic,
)
from pydantic import BaseModel
from utils import get_cached_explanation_for_topic, get_cached_topics_and_explanations

ENV_FILE = os.getenv("APP_ENV", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Ensure that the topic is a string and is required
class ExplainRequestBody(BaseModel):
    topic: str


async def get_rate_limit_key(request: Request) -> str:
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    return f"ratelimit:{token}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.getenv("REDIS_URL")
    redis_client = redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client, identifier=get_rate_limit_key)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/explain", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def explain(
    request: ExplainRequestBody,
    user_and_org=Depends(get_current_user_and_organization),
    can_user_create_topic=Depends(can_user_create_topic),
):
    user, org = user_and_org
    logger.info(f"Received request to explain: {request.topic}")
    if not user or not org or not can_user_create_topic:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Check if the topic is already cached
    cached_explanation = await get_cached_explanation_for_topic(
        request.topic, org.organization_id
    )
    if cached_explanation:
        logger.info("Returning cached explanation")
        return {"response": cached_explanation}
    logger.info("Calling agent...")
    response = await explain_like_im_five(request.topic, org_id=org.organization_id)
    logger.info("Returning agent explanation")
    return {"response": response}


@app.get("/topics-and-explanations")
async def get_topics_and_explanations(
    user_and_org=Depends(get_current_user_and_organization),
    can_user_read_topic=Depends(can_user_read_topic),
):
    user, org = user_and_org
    if not user or not org or not can_user_read_topic:
        logger.warning("Unauthorized access attempt to cached topics")
        raise HTTPException(status_code=401, detail="Unauthorized")
    topics = await get_cached_topics_and_explanations(org.organization_id)
    return topics if topics else []
