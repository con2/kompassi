from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

from core.models.event import Event
from core.models.person import Person

if TYPE_CHECKING:
    from ..models.badge import Badge


class NoopEmperkelator(BaseModel):
    @classmethod
    def emperkelate(
        cls,
        event: Event,
        person: Person,
        existing_badge: Badge | None = None,
    ) -> Self:
        return cls()

    def __str__(self):
        return "N/A"
