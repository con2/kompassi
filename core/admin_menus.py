
from collections import namedtuple


class AdminMenuItem(object):
    __slots__ = ['href', 'text', 'is_active', 'notifications', 'is_admin_menu_item', 'is_mobile_incompatible']

    def __init__(self, href, text, is_active=False, notifications=0, is_mobile_incompatible=False):
        self.href = href
        self.text = text
        self.is_active = is_active
        self.notifications = notifications
        self.is_admin_menu_item = True
        self.is_mobile_incompatible = is_mobile_incompatible

    from core.utils import simple_object_repr as __repr__
