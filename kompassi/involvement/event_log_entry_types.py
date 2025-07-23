from kompassi.event_log_v2 import registry

registry.register(
    name="involvement.invitation.created",
    message="An invitation into {event} was created by {actor}: {email}",
)

# involvement.invitation.used -> involvement.involvement.created(invitation=)

registry.register(
    name="involvement.invitation.revoked",
    message="An invitation into {event} was revoked by {actor}",
)

registry.register(
    name="involvement.involvement.created",
    message="The involvement of {involvement_person} in {event} was created by {actor}: {involvement_description}",
)

# NOTE: don't have access to the involvement object any longer
registry.register(
    name="involvement.involvement.deleted",
    message="The involvement of {involvement_person} in {event} was deleted by {actor}: {involvement_description}",
)
