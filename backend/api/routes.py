from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel
from stytch.core.response_base import StytchError
from core.agent import explain_like_im_five, exchange_code_for_oauth_token
from core.auth import (
    get_current_user_and_organization,
    can_user_create_topic,
    can_user_read_topic,
)
from pydantic import BaseModel
from config.logging_config import logger
from core.cache import (
    get_cached_explanation_for_topic,
    get_cached_topics_and_explanations,
)

router = APIRouter()


class ExplainRequestBody(BaseModel):
    topic: str


@router.post("/explain", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def explain(
    request: ExplainRequestBody,
    user_and_org=Depends(get_current_user_and_organization),
    can_user_create_topic=Depends(can_user_create_topic),
):
    user, org = user_and_org

    if not user or not org or not can_user_create_topic:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.info(f"Received request to explain: {request.topic}")

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


@router.get("/topics-and-explanations")
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
@router.get("/oauth/callback")
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
