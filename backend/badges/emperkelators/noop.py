from typing import Self

from pydantic import BaseModel

from core.models.event import Event
from core.models.person import Person


class NoopEmperkelator(BaseModel):
    @classmethod
    def emperkelate(
        cls,
        event: Event,
        person: Person,
    ) -> Self:
        return cls()

    def __str__(self):
        return "N/A"
