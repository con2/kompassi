from django.utils.translation import gettext_lazy as _

from event_log import registry


registry.register(
    name="tickets.accommodation.presence.arrived",
    message=_("{entry.accommodation_information} arrived in {entry.limit_group.description}"),
)

registry.register(
    name="tickets.accommodation.presence.left",
    message=_("{entry.accommodation_information} left {entry.limit_group.description}"),
)
