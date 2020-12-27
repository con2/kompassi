from django.utils.translation import ugettext_lazy as _

from event_log import registry


registry.register(
    name='access.cbacentry.created',
    message=_('A CBAC entry for {entry.person} was created by {entry.created_by}: {entry.other_fields}'),
)

registry.register(
    name='access.cbacentry.deleted',
    message=_('A CBAC entry for {entry.person} was deleted by {entry.created_by}: {entry.other_fields}'),
)


registry.register(
    name='access.cbac.denied',
    message=_('{entry.created_by} was denied permission by CBAC: {entry.cbac_claims}'),
)

registry.register(
    name='access.cbac.sudo',
    message=_('{entry.created_by} bypassed the permissions check: {entry.cbac_claims}'),
)
