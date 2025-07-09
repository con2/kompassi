from event_log_v2 import registry

registry.register(
    name="core.person.viewed",
    message="The personal information of {person} was viewed by {actor}",
)


registry.register(
    name="core.person.exported",
    message="User {actor} exported personally identifiable information",
)


registry.register(
    name="core.person.impersonated",
    message="User {actor} administratively impersonated {person}",
)


registry.register(
    name="core.password.changed",
    message="User {actor} changed their password",
)
