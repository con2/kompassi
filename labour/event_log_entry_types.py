from django.utils.translation import gettext_lazy as _

from event_log import registry


registry.register(
    name="labour.signup.created",
    message=_("{entry.person} signed up for volunteer work in {entry.event}"),
    email_body_template="labour_signup_created.eml",
)


registry.register(
    name="labour.signup.updated",
    message=_("{entry.person} updated their application for volunteer work in {entry.event}"),
)

registry.register(
    name="labour.signup.archived",
    message=_("The application of {entry.person} for volunteer work in {entry.event} was archived"),
)

registry.register(
    name="labour.signup.deleted",
    message=_("The application of {entry.person} for volunteer work in {entry.event} was deleted"),
)
