from event_log_v2 import registry

registry.register(
    name="forms.response.created",
    message="A form response was created by {actor} for {event}: {response}",
)

registry.register(
    name="forms.response.updated",
    message="A form response was updated by {actor} for {event}: {response}",
)

registry.register(
    name="forms.response.deleted",
    message="A form response was deleted by {actor} for {event}: {response}",
)
