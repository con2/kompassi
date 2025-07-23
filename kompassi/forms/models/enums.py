from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: remove, use ProfileFieldSelector directly
class Anonymity(models.TextChoices):
    # not linked to user account, IP address not recorded
    HARD = "HARD", _("Hard anonymous")
    # linked to user account but not shown to owner, IP address recorded
    SOFT = "SOFT", _("Soft anonymous (linked to user account but not shown to survey owner)")
    # linked to user account and shown to owner, IP address recorded
    NAME_AND_EMAIL = "NAME_AND_EMAIL", _("Name and email shown to survey owner if responded logged-in")
    FULL_PROFILE = "FULL_PROFILE", _("Full profile shown to survey owner if responded logged-in")


class SurveyPurpose(Enum):
    # DEFAULT surveys are answered through the /<event-slug>/<survey-slug> endpoint
    # Responses are handled by create_survey_response mutation (forms application)
    DEFAULT = "DEFAULT"

    # INVITE surveys are answered through the /<event-slug>/invitation/<invitation-id> endpoint
    # Responses are handled by accept_invitation mutation (involvement application)
    INVITE = "INVITE"


class EditMode(Enum):
    # The user is editing items owned by them
    OWNER = "OWNER"

    # An admin is editing items owned by others
    ADMIN = "ADMIN"
