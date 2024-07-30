from event_log_v2 import registry

registry.register(
    name="labour.signup.created",
    message="{person} signed up for volunteer work in {event}",
)


registry.register(
    name="labour.signup.updated",
    message="{person} updated their application for volunteer work in {event}",
)

registry.register(
    name="labour.signup.archived",
    message="The application of {person} for volunteer work in {event} was archived",
)

registry.register(
    name="labour.signup.deleted",
    message="The application of {person} for volunteer work in {event} was deleted",
)
