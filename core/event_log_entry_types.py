from django.utils.translation import ugettext_lazy as _

from event_log import registry


registry.register(
    name='core.person.viewed',
    message=_('The personal information of {entry.person} was viewed by {entry.created_by}'),
)


registry.register(
    name='core.person.exported',
    message=_('User {entry.created_by} exported personally identifiable information'),
)
