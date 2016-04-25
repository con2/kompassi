# encoding: utf-8

from __future__ import unicode_literals

from collections import namedtuple


class AdminMenuItem(object):
    __slots__ = ['href', 'text', 'is_active', 'notifications', 'is_admin_menu_item']

    def __init__(self, href, text, is_active=False, notifications=0):
        self.href = href
        self.text = text
        self.is_active = is_active
        self.notifications = notifications
        self.is_admin_menu_item = True

    from core.utils import simple_object_repr as __repr__