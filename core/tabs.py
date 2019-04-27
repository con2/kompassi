# encoding: utf-8

from collections import namedtuple


class Tab(object):
    __slots__ = [
        'id',
        'title',
        'active',
        'notifications',
    ]

    def __init__(self, id: str, title: str, active=False, notifications=0):
        self.id = id
        self.title = title
        self.active = active
        self.notifications = notifications

    from core.utils import simple_object_repr as __repr__

    @property
    def active_css(self):
        if self.active:
            return 'active'
        else:
            return ''