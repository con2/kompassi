# encoding: utf-8

from collections import namedtuple


BaseTab = namedtuple('Tab', [
    'id',
    'title',
    'active',
])
class Tab(BaseTab):
    @property
    def active_css(self):
        if self.active:
            return 'active'
        else:
            return ''