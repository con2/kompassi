from access.utils import emailify
from labour.models import Signup


def requested_alias(person):
    signup = Signup.objects.filter(event__slug='aicon2018', person=person).first()
    if signup and signup.signup_extra.email_alias:
        return emailify(signup.signup_extra.email_alias.replace('@aicon.fi', ''))

    return None
