from typing import Optional

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import is_within_period, NONUNIQUE_SLUG_FIELD_PARAMS
from core.models import Event

from .form import Form
from ..utils.merge_form_fields import merge_fields


DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class Survey(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

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
            "The form will be available from this date onwards. " "If not set, the form will not be available."
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

    languages = models.ManyToManyField(
        "forms.Form",
        verbose_name=_("language versions"),
        help_text=_(
            "The form will be available in these languages. "
            "Each language can have its own set of fields. "
            "There must be exactly one form per supported language."
        ),
    )

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    def admin_is_active(self):
        return self.is_active

    admin_is_active.short_description = _("active")
    admin_is_active.boolean = True

    @property
    def combined_fields(self):
        return self.get_combined_fields()

    def get_combined_fields(self, base_language: str = DEFAULT_LANGUAGE):
        """
        See ../graphql.py:SurveyType.resolve_combined_fields
        for documentation.
        """
        # TODO as an optimization, store boolean field in survey model that indicates
        # whether the fields are the same across languages. If so, return the fields
        # from the base language directly.

        # if a specific language is requested, put it first
        languages = sorted(
            list(self.languages.all()),
            key=lambda form: form.language != base_language,
        )

        return merge_fields(languages)

    def get_form(self, requested_language: str) -> Optional[Form]:
        try:
            return self.languages.get(language=requested_language)
        except Form.DoesNotExist:
            pass

        for language, _name in settings.LANGUAGES:
            if language == requested_language:
                # already tried above, skip one extra query
                continue

            try:
                return self.languages.get(language=language)
            except Form.DoesNotExist:
                pass

        raise Form.DoesNotExist()

    @property
    def responses(self):
        from .response import Response

        return Response.objects.filter(form__in=self.languages.all()).order_by("created_at")

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return f"{self.event.slug}/{self.slug}"
