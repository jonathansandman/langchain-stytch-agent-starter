from dotenv import load_dotenv

import os
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import sanitize_string, store_topic_and_explanation_in_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine and load environment-specific .env file
# Get the application environment from the environment variable - APP_ENV
app_env = os.getenv("APP_ENV", "local").lower()
env_file = f".env.{app_env}"
env_path = os.path.join(os.path.dirname(__file__), env_file)
load_dotenv(dotenv_path=env_path)

# Note: Ensure you have the OPENAI_API_KEY set in your environment variables
# You can also swap this out for any other LLM provider supported by LangChain
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    timeout=20,
)


def prompt(user_input: str) -> str:
    safe_input = sanitize_string(user_input)
    topic = safe_input.strip()
    if not topic:
        return "Please provide a topic to explain."

    # You can customize this prompt/your instructions to the model as needed
    return f"Explain this to me like I'm 5: {topic}"


async def explain_like_im_five(topic: str, org_id: str) -> str:
    try:
        logger.info(f"Received topic to explain: {topic} for org_id: {org_id}")
        response = await llm.ainvoke([HumanMessage(content=prompt(topic))])
        safe_output = sanitize_string(response.content)
        if safe_output:
            await store_topic_and_explanation_in_cache(topic, safe_output, org_id)
        else:
            logger.warning("LLM returned an empty response, not storing in cache.")

        return safe_output
    except Exception as e:
        logger.error("LLM error: %s", e)
        return "Sorry, I'm out of brain juice right now! Try again later."
