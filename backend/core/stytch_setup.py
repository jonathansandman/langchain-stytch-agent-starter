from stytch import B2BClient
from config.settings import (
    STYTCH_PROJECT_ID,
    STYTCH_SECRET,
    ENVIRONMENT,
)

STYTCH_CLIENT = B2BClient(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment=ENVIRONMENT,
)
