import re


def normalize_whitespace(text: str):
    """Normalize the whitespace in a string."""
    return re.sub(r"\s+", " ", text).strip()
