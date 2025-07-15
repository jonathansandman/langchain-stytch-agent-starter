import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.settings import (
    STYTCH_PROJECT_ID,
    CONNECTED_APP_CLIENT_ID,
    CONNECTED_APP_CLIENT_SECRET,
    CONNECTED_APP_REDIRECT_URI,
    OPEN_AI_KEY,
)
from config.logging_config import logger
from core.cache import (
    store_topic_and_explanation_in_cache,
)
from core.utils import sanitize_string

# Note: Ensure you have the OPENAI_API_KEY set in your environment variables
# You can also swap this out for any other LLM provider supported by LangChain
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPEN_AI_KEY,
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


async def exchange_code_for_oauth_token(code: str):
    url = f"https://test.stytch.com/v1/public/{STYTCH_PROJECT_ID}/oauth2/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CONNECTED_APP_CLIENT_ID,
        "client_secret": CONNECTED_APP_CLIENT_SECRET,
        "redirect_uri": CONNECTED_APP_REDIRECT_URI,
    }

    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
