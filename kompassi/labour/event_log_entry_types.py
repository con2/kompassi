from kompassi.event_log_v2 import registry

registry.register(
    name="labour.signup.created",
    message="{person} signed up for volunteer work in {event}",
)


registry.register(
    name="labour.signup.updated",
    message="The volunteer work application for {person} in {event} was updated by {actor}",
)

registry.register(
    name="labour.signup.archived",
    message="The application of {person} for volunteer work in {event} was archived",
)

registry.register(
    name="labour.signup.deleted",
    message="The application of {person} for volunteer work in {event} was deleted",
)
