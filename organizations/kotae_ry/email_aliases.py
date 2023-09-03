import logging

from access.email_aliases import nick
from access.utils import emailify
from labour.models import Signup


logger = logging.getLogger("kompassi")


def requested_alias_or_nick(person):
    signup = Signup.objects.filter(event__organization__slug="kotae-ry", person=person).order_by("-created_at").first()
    if signup and signup.signup_extra.email_alias:
        try:
            return emailify(signup.signup_extra.email_alias.replace("@kotae.fi", ""))
        except Exception:
            logger.error("Failed to emailify Kotae person %s", signup, exc_info=True)
            # fall-through is intended

    return nick(person)
