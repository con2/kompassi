from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EnrollmentConfig(AppConfig):
    name = "kompassi.zombies.enrollment"
    verbose_name = _("Enrollment")
