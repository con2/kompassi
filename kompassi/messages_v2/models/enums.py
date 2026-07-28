from __future__ import annotations

from enum import Enum


class MessageApp(Enum):
    """
    Records which product owns a Message. Only PROGRAM is used for now;
    the enum reserves room for forms/involvement/volunteers to reuse Messages V2 later.
    """

    PROGRAM = "program_v2"


class MessageDispatch(Enum):
    PER_PERSON = "per_person"
    PER_INVOLVEMENT = "per_involvement"


class MessageState(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
