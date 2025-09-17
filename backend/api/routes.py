from fastapi import APIRouter, Request, Depends, HTTPException, Header, Query
from fastapi.responses import RedirectResponse
from fastapi_limiter.depends import RateLimiter
from pydantic import BaseModel
from stytch.core.response_base import StytchError
from core.agent import explain_like_im_five
from core.auth import (
    get_current_user_and_organization,
    can_user_create_topic,
    can_user_read_topic,
    verify_access_token,
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


@router.get("/explanations")
async def get_explanations_for_cli(
    authorization: str = Header(...),
    limit: int = Query(default=10, le=50)
):
    """Get explanation history for CLI clients using access tokens"""

    # Extract access token (NOT session token)
    access_token = authorization.removeprefix("Bearer ").strip()

    try:
        # Verify access token with Stytch
        user_data = verify_access_token(access_token)

        if not user_data or not user_data.get('organization_id'):
            raise HTTPException(status_code=401, detail="Invalid token or missing organization")

        # Get explanations for this organization
        explanations = await get_cached_topics_and_explanations(user_data['organization_id'])

        # Limit results
        limited_explanations = (explanations or [])[:limit]

        return limited_explanations

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CLI API error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch explanations")


