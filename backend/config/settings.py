import os
from dotenv import load_dotenv

APP_ENV = os.getenv("APP_ENV", "local")
env_path = os.path.join(os.path.dirname(__file__), f"../.env.{APP_ENV}")
load_dotenv(dotenv_path=env_path)

REDIS_URL = os.getenv("REDIS_URL")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
ENVIRONMENT = "live" if APP_ENV == "production" else "test"
