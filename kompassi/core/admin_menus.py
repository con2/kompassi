from dataclasses import dataclass
from typing import Any


@dataclass
class AdminMenuItem:
    href: str
    text: Any  # str or translation promise
    is_active: bool = False
    notifications: int = 0
    is_mobile_incompatible: bool = False

    is_admin_menu_item = True
