from access.email_aliases import nick
from access.utils import emailify
from labour.models import Signup


def requested_alias_or_nick(person):
    signup = Signup.objects.filter(event__slug='tracon11', person=person)
    if signup:
        if signup.signup_extra.email_alias:
            return emailify(signup.signup_extra.email_alias)
    else:
        return nick(person)