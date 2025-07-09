from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .models import EntryTypeMetadata

entry_types = dict()


def register(
    name: str,
    message: str,
    email_body_template: str | None = None,
    email_reply_to: Sequence[str] | Callable[[Any], Sequence[str]] | None = None,
) -> EntryTypeMetadata:
    from .models import EntryTypeMetadata

    entry_types[name] = EntryTypeMetadata(
        name=name,
        message=message,
        email_body_template=email_body_template,
        email_reply_to=email_reply_to,
    )
    return entry_types[name]


def get(entry_type_name: str) -> EntryTypeMetadata:
    return entry_types[entry_type_name]
