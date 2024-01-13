from django.utils.translation import gettext_lazy as _

LOW_AVAILABILITY_THRESHOLD = 10
UNPAID_CANCEL_HOURS = 24
TICKETS_VIEW_VERSION_CHOICES = [
    ("v1", "Version 1 (Django frontend, multiple phases)"),
    ("v1.5", "Version 1.5 (Django frontend, single phase)"),
    ("v2", "Version 2 (Next.js frontend)"),
]
# note: corresponding message templates must be under templates/email/LANGUAGE_CODE/
LANGUAGE_CHOICES = [
    ("fi", _("Finnish")),
    ("en", _("English")),
]
