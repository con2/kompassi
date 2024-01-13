from event_log.utils import log_creations

from ..models import Signup

log_creations(
    Signup,
    person=lambda signup: signup.person,
    created_by=lambda signup: signup.person.user,
)
