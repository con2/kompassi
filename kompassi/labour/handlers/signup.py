from kompassi.event_log_v2.utils.emit import log_creations

from ..models import Signup

log_creations(
    Signup,
    person=lambda signup: signup.person.id,
    actor=lambda signup: signup.person.user,
    event=lambda signup: signup.event.slug,
    organization=lambda signup: signup.event.organization.slug,
)
