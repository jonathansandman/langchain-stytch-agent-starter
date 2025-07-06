import os
import logging
from fastapi import HTTPException, Header
from cachetools import TTLCache
from stytch import B2BClient
from stytch.core.response_base import StytchError

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

token_cache = TTLCache(maxsize=500, ttl=300)

can_user_create_topic_auth_check = {
    "resource": "explain.topic",
    "action": "create",
}

can_user_read_topic_auth_check = {
    "resource": "explain.topic",
    "action": "read",
}


def can_user_create_topic(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    try:
        data = verify_session_token(token, auth_check=can_user_create_topic_auth_check)
        if not data.member or not data.organization:
            logger.error("User or organization not found in session")
            raise HTTPException(status_code=401, detail="Auth error")
        return True
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Auth error")


def can_user_read_topic(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    try:
        data = verify_session_token(token, auth_check=can_user_read_topic_auth_check)
        if not data.member or not data.organization:
            logger.error("User or organization not found in session")
            raise HTTPException(status_code=401, detail="Auth error")
        return True
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Auth error")


def get_current_user_and_organization(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    try:
        data = verify_session_token(token)
        if not data.member or not data.organization:
            logger.error("User or organization not found in session")
            raise HTTPException(status_code=401, detail="Auth error")
        return data.member, data.organization
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Auth error")


def verify_session_token(token: str, auth_check=None) -> dict:
    options = {}

    if token in token_cache:
        return token_cache[token]

    options["session_token"] = token
    if auth_check:
        options["auth_check"] = auth_check

    try:
        response = client.sessions.authenticate(**options)
        token_cache[token] = response
        return response
    except StytchError as e:
        logger.error(f"Stytch API error: {e}")
        raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        logger.error(f"Unexpected auth error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")
