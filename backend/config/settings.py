import os
from dotenv import load_dotenv

APP_ENV = os.getenv("APP_ENV", "local")
env_path = os.path.join(os.path.dirname(__file__), f"../.env.{APP_ENV}")
load_dotenv(dotenv_path=env_path)

REDIS_URL = os.getenv("REDIS_URL")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")

CONNECTED_APP_CLIENT_ID = os.getenv("CONNECTED_APP_CLIENT_ID")
CONNECTED_APP_CLIENT_SECRET = os.getenv("CONNECTED_APP_CLIENT_SECRET")
CONNECTED_APP_REDIRECT_URI = os.getenv("CONNECTED_APP_REDIRECT_URI")

STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
ENVIRONMENT = "live" if APP_ENV == "production" else "test"
