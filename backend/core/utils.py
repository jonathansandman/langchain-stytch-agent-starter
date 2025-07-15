import re


def sanitize_string(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove control characters and other suspicious invisible chars
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # Optionally, trim long whitespace or weird characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
