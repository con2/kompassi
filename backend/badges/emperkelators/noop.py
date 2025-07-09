from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

if TYPE_CHECKING:
    from ..models.badge import Badge


class NoopEmperkelator(BaseModel):
    @classmethod
    def emperkelate(cls, badge: Badge) -> Self:
        return cls()

    def __str__(self):
        return "N/A"
