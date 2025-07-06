import re
import redis.asyncio as redis
import os


def redis_client() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    raise ValueError("REDIS_URL environment variable is not set.")


async def store_topic_and_explanation_in_cache(
    topic: str, explanation: str, org_id: str
) -> None:
    if not topic:
        return

    client = redis_client()
    cache_key = f"org:{org_id}:topics:{topic.lower().replace(' ', '_')}"
    # Store the explanation in a list, with the most recent at the front
    await client.set(cache_key, explanation, ex=604800)


async def get_cached_explanation_for_topic(topic: str, org_id: str) -> str | None:
    client = redis_client()
    cache_key = f"org:{org_id}:topics:{topic.lower().replace(' ', '_')}"
    # cached_explanation = client.lrange(cache_key, 0, -1)
    cached_explanation = await client.get(cache_key)
    if cached_explanation:
        return cached_explanation  # Return the most recent explanation
    return None


async def get_cached_topics_and_explanations(org_id: str) -> list[dict[str, str]]:
    client = redis_client()
    cache_key_pattern = f"org:{org_id}:topics:*"
    keys = await client.keys(cache_key_pattern)
    topics = []
    for key in keys:
        topic = key.split(":")[-1].replace("_", " ")
        explanation = await client.get(key)
        if explanation:
            topics.append({"topic": topic, "explanation": explanation})
    return topics


def sanitize_string(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove control characters and other suspicious invisible chars
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # Optionally, trim long whitespace or weird characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
