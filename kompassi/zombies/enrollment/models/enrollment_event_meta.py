from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import EventMetaBase
from kompassi.core.utils import is_within_period

INITIAL_STATE_CHOICES = [
    ("NEW", _("New")),
    ("ACCEPTED", _("Accepted")),
]


class EnrollmentEventMeta(EventMetaBase):
    """
    An event has an instance of this class to indicate use of the enrollment module.
    """

    form_class_path = models.CharField(
        max_length=63,
        help_text=_("Reference to form class. Example: events.yukicon2016.forms:EnrollmentForm"),
    )

    enrollment_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enrollment opens"),
    )

    enrollment_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enrollment closes"),
    )

    override_enrollment_form_message = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Enrollment form message"),
        help_text=_(
            "Use this field to override the message that is shown in top of the enrollment form. "
            "If this field is not filled in, a default message is shown."
        ),
    )

    is_participant_list_public = models.BooleanField(
        default=False,
        verbose_name=_("Participant list is public"),
        help_text=_(
            "If this option is selected, the names of participants who have given the permission to do so "
            "will be published."
        ),
    )

    is_official_name_required = models.BooleanField(
        default=False,
        verbose_name=_("Official name required"),
        help_text=_(
            "If this option is selected, participants will be required to fill in their official names "
            "in their profile."
        ),
    )

    initial_state = models.CharField(
        default="ACCEPTED",
        choices=INITIAL_STATE_CHOICES,
        max_length=max(len(key) for (key, label) in INITIAL_STATE_CHOICES),
        verbose_name=_("Initial state"),
        help_text=_("Change this to New to require approval for new enrollments."),
    )

    @property
    def form_class(self):
        return None

    @property
    def is_enrollment_open(self):
        return is_within_period(self.enrollment_opens, self.enrollment_closes)

    @property
    def is_public(self):
        """
        Alias used by generic_start_stop_view
        """
        return self.is_enrollment_open

    @property
    def enrollment_form_message(self):
        return self.override_enrollment_form_message
        # else:
        #     return _(
        #         'Using this form you can enroll in the event. Please note that filling in the form '
        #         'does not guarantee automatic admittance into the event. You will be contacted by '
        #         'the event organizer and notified of the decision whether to accept your enrollment '
        #         'or not.'
        #     )

    def publish(self):
        """
        Used by the start/stop enrollment period view to start the enrollment period. Returns True
        if the user needs to be warned about a certain corner case where information was lost.
        """
        warn = False
        t = now()

        if self.enrollment_closes and self.enrollment_closes <= t:
            self.enrollment_closes = None
            warn = True

        self.enrollment_opens = t
        self.save()

        return warn

    def unpublish(self):
        """
        Used by the start/stop enrollment period view to end the enrollment period. We prefer setting
        enrollment_closes to clearing enrollment_opens because this causes less information loss.
        """
        self.enrollment_closes = now()
        self.save()

    def get_form_field_headers(self):
        return []
