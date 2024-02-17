from __future__ import annotations

import logging
from copy import deepcopy
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS
from core.utils.locale_utils import get_message_in_language

from .field import Field

if TYPE_CHECKING:
    from program_v2.models.offer_form import OfferForm

    from .response import Response
    from .survey import Survey


logger = logging.getLogger("kompassi")

LAYOUT_CHOICES = [
    ("horizontal", _("Horizontal")),
    ("vertical", _("Vertical")),
]

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class Form(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="forms")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    title = models.CharField(max_length=255, default="")
    description = models.TextField(blank=True, default="")
    thank_you_message = models.TextField(blank=True, default="")
    language = models.CharField(max_length=2, default=DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    layout = models.CharField(
        verbose_name=_("Layout"),
        choices=LAYOUT_CHOICES,
        max_length=max(len(c) for (c, t) in LAYOUT_CHOICES),
        default=LAYOUT_CHOICES[0][0],
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields = models.JSONField(default=list)

    # cached fields
    cached_enriched_fields = models.JSONField(default=list)

    # related fields
    responses: models.QuerySet[Response]

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return self.title

    @property
    def can_remove(self):
        # TODO(#432) Revisit criteria for can_remove
        return not self.responses.exists()

    @property
    def enriched_fields(self) -> list[dict[str, Any]]:
        """
        There is a chicken and egg problem with the enriched_fields property, mostly when
        Forms, Surveys and Dimensions are created programmatically (eg. in tests and setup scripts).
        If a `valueFrom` directive is used in a Field, the Form needs to belong to a Survey.
        """
        if not self.cached_enriched_fields:
            self.refresh_enriched_fields()

        return self.cached_enriched_fields

    @classmethod
    @transaction.atomic
    def refresh_enriched_fields_qs(cls, qs: models.QuerySet[Self]):
        """
        Refresh cached_enriched_fields for all forms in the queryset.
        """
        forms_to_update = []
        for form in qs.select_for_update(of=("self",)):
            form.cached_enriched_fields = form._build_enriched_fields()
            forms_to_update.append(form)
        cls.objects.bulk_update(forms_to_update, ["cached_enriched_fields"])

    def refresh_enriched_fields(self):
        """
        Refresh cached_enriched_fields for this form.
        NOTE: Use refresh_enriched_fields_qs for bulk updates.
        """
        self.cached_enriched_fields = self._build_enriched_fields()
        self.save(update_fields=["cached_enriched_fields"])

    def _build_enriched_fields(self) -> list[dict[str, Any]]:
        return [self._enrich_field(field) for field in self.fields]

    def _enrich_field(self, field: dict[str, Any]) -> dict[str, Any]:
        """
        Some field types may contain server side directives that need to be resolved before
        turning the form specification over to the frontend.
        """
        from forms.models.dimension import Dimension as SurveyDimension
        from program_v2.models.dimension import Dimension as ProgramDimension

        field = deepcopy(field)

        if choices_from := field.get("choicesFrom"):
            field["choices"] = []

            if len(choices_from) != 1:
                raise ValueError("choicesFrom must have exactly one key: value pair")

            ((source_type, source),) = choices_from.items()
            if source_type == "dimension":
                # TODO store use_case or similar on Form to avoid trying all use cases in a loop
                if survey := self.survey:
                    # form used as survey form
                    try:
                        dimension = SurveyDimension.objects.get(survey=survey, slug=source)
                        field["choices"] = [
                            choice.model_dump(by_alias=True) for choice in dimension.get_choices(self.language)
                        ]
                    except SurveyDimension.DoesNotExist:
                        logger.warning(f"Survey dimension {source} does not exist on survey {survey}")
                elif self.offer_form:
                    # form used as program signup form
                    try:
                        dimension = ProgramDimension.objects.get(event=self.event, slug=source)
                        field["choices"] = [
                            dict(
                                slug=value_slug,
                                title=get_message_in_language(value_title, self.language),
                            )
                            for value_slug, value_title in dimension.values.all().values_list("slug", "title")
                        ]
                    except ProgramDimension.DoesNotExist:
                        logger.warning(f"Program dimension {source} does not exist on event {self.event}")

                else:
                    raise ValueError("A form that is not used as a survey or program offer form cannot use valuesFrom")

            else:
                raise NotImplementedError(f"choicesFrom: {choices_from}")

            del field["choicesFrom"]

        return field

    @cached_property
    def validated_fields(self):
        return [Field.model_validate(field_dict) for field_dict in self.enriched_fields]

    @property
    def survey(self) -> Survey | None:
        from .survey import Survey

        # there can only be one
        try:
            return self.event.surveys.get(languages=self)
        except Survey.DoesNotExist:
            return None
        except Survey.MultipleObjectsReturned:
            raise

    @property
    def offer_form(self) -> OfferForm | None:
        from program_v2.models.offer_form import OfferForm

        # there can only be one
        try:
            return OfferForm.objects.get(event=self.event, languages=self)
        except OfferForm.DoesNotExist:
            return None
        except OfferForm.MultipleObjectsReturned:
            raise
