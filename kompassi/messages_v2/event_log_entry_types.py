from kompassi.event_log_v2 import registry

registry.register(
    name="messages_v2.message.created",
    message="A message draft for {event} was created by {actor}: {message_id}",
)

registry.register(
    name="messages_v2.message.edited",
    message="A message for {event} was edited by {actor}: {message_id}",
)

registry.register(
    name="messages_v2.message.sent",
    message="A message for {event} was sent by {actor} to {initial_recipients} recipients: {message_id}",
)

registry.register(
    name="messages_v2.message.expired",
    message="A message for {event} was expired by {actor}: {message_id}",
)

registry.register(
    name="messages_v2.message.deleted",
    message="A message draft for {event} was deleted by {actor}: {message_id}",
)
