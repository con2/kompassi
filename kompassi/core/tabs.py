from dataclasses import dataclass
from typing import Any


@dataclass
class Tab:
    id: str
    title: Any  # str or translation promise
    active: bool = False
    notifications: int = 0

    @property
    def active_css(self):
        if self.active:
            return "active"
        else:
            return ""
