from django.utils.translation import gettext_lazy as _

from event_log import registry


registry.register(
    name="membership.membership.created",
    message=_("New membership application"),
    email_body_template="membership_application_notification.eml",
)
