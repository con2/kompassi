from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, is_within_period
from forms.models.form import Form
from graphql_api.language import SUPPORTED_LANGUAGES


class OfferForm(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="program_offer_forms")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    short_description = HStoreField(blank=True, default=dict)

    languages = models.ManyToManyField(
        Form,
        verbose_name=_("language versions"),
        help_text=_(
            "The form will be available in these languages. "
            "Each language can have its own set of fields. "
            "There must be exactly one form per supported language."
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

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    def get_form(self, requested_language: str) -> Form:
        try:
            return self.languages.get(language=requested_language)
        except Form.DoesNotExist:
            pass

        for language in SUPPORTED_LANGUAGES:
            if language.code == requested_language:
                # already tried above, skip one extra query
                continue

            try:
                return self.languages.get(language=language.code)
            except Form.DoesNotExist:
                pass

        raise Form.DoesNotExist()

    class Meta:
        unique_together = [
            ("event", "slug"),
        ]
