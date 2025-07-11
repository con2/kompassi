from event_log_v2 import registry

registry.register(
    name="access.cbacentry.created",
    message="A CBAC entry for {user} was created by {actor}: {claims}",
)

registry.register(
    name="access.cbacentry.deleted",
    message="A CBAC entry for {user} was deleted by {actor}: {claims}",
)

registry.register(
    name="access.cbacentry.expired",
    message="A CBAC entry for {user} expired and was deleted: {claims}",
)


registry.register(
    name="access.cbac.denied",
    message="{actor} was denied permission by CBAC: {claims}",
)

registry.register(
    name="access.cbac.sudo",
    message="{actor} bypassed the permissions check: {claims}",
)
