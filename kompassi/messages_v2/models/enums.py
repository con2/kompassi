from __future__ import annotations

from enum import Enum


class MessageDispatch(Enum):
    PER_PERSON = "per_person"
    PER_INVOLVEMENT = "per_involvement"


class MessageState(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EXPIRED = "expired"
