from typing import Any


def section(title: str, content: Any) -> dict:
    return {
        "type": "Section",
        "title": title,
        "content": content,
    }
