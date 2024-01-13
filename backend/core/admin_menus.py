from dataclasses import dataclass


@dataclass
class AdminMenuItem:
    href: str
    text: str
    is_active: bool = False
    notifications: int = 0
    is_mobile_incompatible: bool = False

    is_admin_menu_item = True
