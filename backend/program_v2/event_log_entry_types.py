from event_log_v2 import registry

registry.register(
    name="program_v2.program.created",
    message="A program item in {event} was created by {actor}: {program}",
)

registry.register(
    name="program_v2.program.updated",
    message="A program item in {event} was updated by {actor}: {program}",
)

registry.register(
    name="program_v2.program.cancelled",
    message="A program item in {event} was cancelled by {actor}: {program}",
)

# program offer created -> forms.response.created
# program host invited -> involvement.invitation.created
# program host invitation accepted -> involvement.invitation.accepted
