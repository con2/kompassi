from event_log_v2 import registry

# TODO(2025/04) remove once 2024/09 partition has been reaped
registry.register(
    name="tickets.accommodation.presence.arrived",
    message="{accommodation_information} arrived in {limit_group}",
)

registry.register(
    name="tickets.accommodation.presence.left",
    message="{accommodation_information} left {limit_group}",
)
