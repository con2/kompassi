from typing import Optional

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import is_within_period, SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS
from core.models import Event

from .form import EventForm, GlobalForm


class AbstractSurvey(models.Model):
    active = models.BooleanField(default=True)
    standalone = models.BooleanField(
        default=True,
        verbose_name=_("Stand-alone"),
        help_text=_(
            "Stand-alone forms can be used via the generic form views whereas "
            "non-stand-alone forms can only be accessed from some other facility."
        ),
    )
    login_required = models.BooleanField(
        default=False,
        verbose_name=_("Login required"),
        help_text=_(
            "This switch only takes effect in a stand-alone context. In non-stand-alone "
            "contexts the use case will direct whether or not login is required."
        ),
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("active from"),
        help_text=_(
            "The form will be available from this date onwards. "
            "If not set, the form will not be available."
        ),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("active until"),
        help_text=_(
            "The form will be available until this date. "
            "If not set, the form will be available indefinitely "
            "provided that active_from is set and has passed."
        ),
    )

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    class Meta:
        abstract = True


class GlobalSurvey(AbstractSurvey):
    slug = models.CharField(**SLUG_FIELD_PARAMS)  # type: ignore

    languages = models.ManyToManyField(
        GlobalForm,
        verbose_name=_("language versions"),
        help_text=_(
            "The form will be available in these languages. "
            "Each language can have its own set of fields. "
            "There must be exactly one form per supported language."
        ),
    )

    def get_form(self, requested_language: str) -> Optional[GlobalForm]:
        try:
            return self.languages.get(language=requested_language)
        except GlobalForm.DoesNotExist:
            pass

        for language, _ in settings.LANGUAGES:
            if language == requested_language:
                # already tried above, skip one extra query
                continue

            try:
                return self.languages.get(language=language)
            except GlobalForm.DoesNotExist:
                pass

        raise GlobalForm.DoesNotExist()

    def __str__(self):
        return self.slug


class EventSurvey(AbstractSurvey):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    languages = models.ManyToManyField(
        "forms.EventForm",
        verbose_name=_("language versions"),
        help_text=_(
            "The form will be available in these languages. "
            "Each language can have its own set of fields. "
            "There must be exactly one form per supported language."
        ),
    )

    def get_form(self, requested_language: str) -> Optional[EventForm]:
        try:
            return self.languages.get(language=requested_language)
        except EventForm.DoesNotExist:
            pass

        for language, _ in settings.LANGUAGES:
            if language == requested_language:
                # already tried above, skip one extra query
                continue

            try:
                return self.languages.get(language=language)
            except EventForm.DoesNotExist:
                pass

        raise EventForm.DoesNotExist()

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return f"{self.event.slug}/{self.slug}"
