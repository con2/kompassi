from typing import Optional


from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from localized_fields.models import LocalizedModel
from localized_fields.fields import LocalizedTextField

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS
from forms.models.form import EventForm


class OfferForm(LocalizedModel):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="program_offer_forms")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    short_description = LocalizedTextField(
        blank=True,
        default=dict,
        verbose_name=_("short description"),
        help_text=_("Visible on the page that offers different kinds of forms."),
    )

    languages: models.QuerySet["OfferFormLanguage"]

    def get_form(self, requested_language: str) -> Optional[EventForm]:
        try:
            return self.languages.get(language_code=requested_language).form
        except OfferFormLanguage.DoesNotExist:
            pass

        for language_code, _ in settings.LANGUAGES:
            if language_code == requested_language:
                # already tried above, skip one extra query
                continue

            try:
                return self.languages.get(language_code=language_code).form
            except OfferFormLanguage.DoesNotExist:
                pass

        return None

    class Meta:
        unique_together = [
            ("event", "slug"),
        ]


class OfferFormLanguage(models.Model):
    offer_form = models.ForeignKey(
        OfferForm,
        on_delete=models.CASCADE,
        related_name="languages",
    )

    language_code = models.CharField(
        max_length=2,
        verbose_name=_("language"),
    )

    form = models.ForeignKey(
        "forms.EventForm",
        on_delete=models.CASCADE,
        related_name="+",
    )
