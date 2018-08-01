from django.utils.translation import ugettext_lazy as _

from event_log import registry


registry.register(
    name='directory.search.performed',
    message=_('User {entry.created_by} searched the {entry.organization} directory for: {entry.search_term}'),
)


registry.register(
    name='directory.viewed',
    message=_('User {entry.created_by} browsed the {entry.organization} directory without a search term.'),
)
