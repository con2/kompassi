from collections.abc import Callable, Sequence
from typing import Any

from pydantic import BaseModel

from ..registry import get, register


class EntryTypeMetadata(BaseModel):
    name: str
    message: str | Callable[[Any], str] = "An event of type {entry_type} occurred"
    email_body_template: str | None = None
    email_reply_to: Sequence[str] | Callable[[Any], Sequence[str]] | None = ()

    @classmethod
    def get_or_create_dummy(cls, name="eventlog.dummy", **attrs):
        try:
            return get(name), False
        except KeyError:
            return register(name, **attrs), True
