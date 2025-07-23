from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils.misc_utils import get_code
from kompassi.core.utils.model_utils import NONUNIQUE_SLUG_FIELD_PARAMS
from kompassi.core.utils.time_utils import is_within_period


class Survey(models.Model):
    """
    The Labour Manager may have their Workers fill in a Survey some time after signing up.
    The driving use case for these Surveys is to ask for shift wishes some time before the event.
    A Survey requires a Model and a Form. The Model is requested to return an instance via
    Model.for_signup(signup) and it is passed to the Form via
    initialize_form(Form, request, instance=instance, event=event).
    """

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="labour_surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Will be displayed at the top of the survey page."),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Will be displayed at the top of the survey page."),
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active from"),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active until"),
    )

    form_class_path = models.CharField(
        max_length=255,
        verbose_name=_("Form path"),
        help_text=_("A reference to the form that is used as the survey form."),
    )

    override_does_not_apply_message = models.TextField(
        default="",
        verbose_name=_("Message when denied access"),
        help_text=_(
            "This message will be shown to the user when they attempt to access a query they don'thave access to."
        ),
    )

    def __str__(self):
        return self.title

    @property
    def form_class(self):
        cp = self.form_class_path
        if not cp.startswith("kompassi."):
            cp = f"kompassi.{cp}"
        return get_code(cp)

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    @property
    def does_not_apply_message(self):
        if self.override_does_not_apply_message:
            return self.override_does_not_apply_message
        else:
            return _("This survey does not apply to you.")

    def admin_is_active(self):
        return self.is_active

    admin_is_active.short_description = "Active"  # type: ignore
    admin_is_active.boolean = True  # type: ignore

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")
        unique_together = [
            ("event", "slug"),
        ]


class SurveyRecord(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="survey_records")
    person = models.ForeignKey("core.Person", on_delete=models.CASCADE, related_name="survey_records")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.person.full_name if self.person else "None"
