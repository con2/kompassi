from dataclasses import dataclass


@dataclass
class Tab:
    id: str
    title: str
    active: bool = False
    notifications: int = 0

    @property
    def active_css(self):
        if self.active:
            return "active"
        else:
            return ""
