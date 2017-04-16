# encoding: utf-8

from django.utils.translation import ugettext_lazy as _


class EntryTypeMetadata(object):
    __slots__ = [
        'name',
        'message',
        'email_body_template',
        'email_reply_to',
    ]

    def __init__(
        self,
        name,
        message=lambda entry: _('An event of type {entry.entry_type} occurred').format(entry=entry),
        email_body_template='event_log_default.eml',
        email_reply_to=None,
        get_event=lambda instance: instance.event,
    ):
        self.name = name
        self.message = message
        self.email_body_template = email_body_template
        self.email_reply_to = email_reply_to

    @classmethod
    def get_or_create_dummy(self, name='eventlog.dummy', **attrs):
        from ..registry import register, get

        try:
            return get(name), False
        except KeyError:
            return register(name, **attrs), True
