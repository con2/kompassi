from django.utils.translation import ugettext_lazy as _

from event_log import registry


registry.register(
    name='labour.signup.created',
    message=_('{entry.person} signed up for volunteer work in {entry.event}'),
)


registry.register(
    name='labour.signup.updated',
    message=_('{entry.person} updated their application for volunteer work in {entry.event}'),
)
