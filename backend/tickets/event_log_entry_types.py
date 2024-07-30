from event_log_v2 import registry

registry.register(
    name="tickets.accommodation.presence.arrived",
    message="{accommodation_information} arrived in {limit_group}",
)

registry.register(
    name="tickets.accommodation.presence.left",
    message="{accommodation_information} left {limit_group}",
)
