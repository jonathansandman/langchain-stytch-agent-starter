from fastapi import HTTPException, Header
from cachetools import TTLCache
from stytch.core.response_base import StytchError
from config.stytch_client import STYTCH_CLIENT
from config.logging_config import logger

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
        response = STYTCH_CLIENT.sessions.authenticate(**options)
        token_cache[token] = response
        return response
    except StytchError as e:
        logger.error(f"Stytch API error: {e}")
        raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        logger.error(f"Unexpected auth error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")


def verify_access_token(access_token: str) -> dict:
    """Verify OAuth access token from Connected Apps (CLI)"""
    try:
        # Use Stytch's built-in Connected Apps token introspection (local validation)
        response = STYTCH_CLIENT.idp.introspect_access_token_local(access_token)


        # Check if response is None (invalid token)
        if response is None:
            logger.error("Token introspection returned None - invalid token")
            raise HTTPException(status_code=401, detail="Invalid access token")

        # Extract user and organization info from introspection response
        # The response is an IDPTokenClaims object
        user_id = getattr(response, 'subject', None)
        org_claim = getattr(response, 'organization_claim', {})
        organization_id = org_claim.get('organization_id') if org_claim else None

        if not user_id or not organization_id:
            logger.error(f"Missing required user_id ({user_id}) or organization_id ({organization_id}) in token")
            raise HTTPException(status_code=401, detail="Invalid token claims")

        return {
            'user_id': user_id,
            'organization_id': organization_id,
            'scopes': getattr(response, 'scope', '').split(' ') if getattr(response, 'scope', '') else []
        }

    except StytchError as e:
        logger.error(f"Access token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(status_code=401, detail="Invalid access token")
