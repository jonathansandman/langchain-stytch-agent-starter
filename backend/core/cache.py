from config.redis import redis_client


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
