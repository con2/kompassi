from django.utils.translation import gettext_lazy as _

LOW_AVAILABILITY_THRESHOLD = 10
UNPAID_CANCEL_HOURS = 24
# note: corresponding message templates must be under templates/email/LANGUAGE_CODE/
LANGUAGE_CHOICES = [
    ("fi", _("Finnish")),
    ("en", _("English")),
]
