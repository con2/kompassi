# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from collections import namedtuple


ENTRY_TYPE_DEFAULTS = dict(
    message=lambda entry: _('An event of type {entry.entry_type} occurred').format(entry=entry),
    email_body_template='event_log_default.eml',
    email_reply_to=None,
)


BaseEntryTypeMetadata = namedtuple('EntryTypeMetadata', [
    'name',
    'message',
    'email_body_template',
    'email_reply_to',
])


class EntryTypeMetadata(BaseEntryTypeMetadata):
    def __init__(self, **kwargs):
        attrs = dict(ENTRY_TYPE_DEFAULTS, **kwargs)
        super(EntryTypeMetadata, self).__init__(**attrs)
