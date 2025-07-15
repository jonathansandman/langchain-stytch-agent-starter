import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import RedirectResponse

from stytch import B2BClient
from stytch.core.response_base import StytchError

from contextlib import asynccontextmanager
import redis.asyncio as redis
from agent import explain_like_im_five, exchange_code_for_oauth_token
from auth import (
    get_current_user_and_organization,
    can_user_create_topic,
    can_user_read_topic,
)
from pydantic import BaseModel
from utils import get_cached_explanation_for_topic, get_cached_topics_and_explanations

ENV_FILE = os.getenv("APP_ENV", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
APP_ENV = os.getenv("APP_ENV", "local")
ENVIRONMENT = "test" if APP_ENV != "production" else "live"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = B2BClient(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment=ENVIRONMENT,
)


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


# Consent and grant scopes to Explain like I'm Five agent
# Our backend is acting as a Connected App
@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        logger.error("No code provided in OAuth callback")
        raise HTTPException(status_code=400, detail="Missing code parameter")

    try:
        token_data = await exchange_code_for_oauth_token(code)
        if not token_data or "access_token" not in token_data:
            logger.error("Invalid token data received from OAuth exchange")
            raise HTTPException(status_code=500, detail="Invalid token data")
        logger.info("OAuth token exchange successful")
        return RedirectResponse(url="http://localhost:5173/dashboard")
    except StytchError as e:
        logger.error(f"OAuth token exchange failed: {e}")
        raise HTTPException(status_code=500, detail="OAuth token exchange failed")
    except Exception as e:
        logger.error(f"Unexpected error during OAuth callback: {e}")
        raise HTTPException(
            status_code=500, detail="Unexpected error during OAuth callback"
        )
