from event_log_v2 import registry

registry.register(
    name="membership.membership.created",
    message="New membership application for {organization}: {person}",
)
