from __future__ import annotations

import logging
from collections.abc import Collection, Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

import yaml
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, is_within_period, log_get_or_create
from core.utils.pkg_resources_compat import resource_stream
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

from ..utils.merge_form_fields import merge_fields
from .form import Form

if TYPE_CHECKING:
    from .dimension import Dimension, DimensionValue

logger = logging.getLogger("kompassi")
ANONYMITY_CHOICES = [
    # not linked to user account, IP address not recorded
    ("hard", _("Hard anonymous")),
    # linked to user account but not shown to owner, IP address recorded
    ("soft", _("Soft anonymous (linked to user account but not shown to survey owner)")),
    # linked to user account and shown to owner, IP address recorded
    ("name_and_email", _("Name and email shown to survey owner if responded logged-in")),
]


class Survey(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    login_required = models.BooleanField(
        default=False,
        verbose_name=_("Login required"),
    )

    max_responses_per_user = models.PositiveIntegerField(
        default=0,
        verbose_name=_("max responses per user"),
        help_text=_(
            "Maximum number of responses per user. 0 = unlimited. "
            "Note that if login_required is not set, this only takes effect for logged in users."
            "Has no effect if the survey is hard anonymous."
        ),
    )

    anonymity = models.CharField(
        max_length=max(len(key) for key, _ in ANONYMITY_CHOICES),
        choices=ANONYMITY_CHOICES,
        default="soft",
        verbose_name=_("anonymity"),
        help_text=_(
            "Hard anonymous: responses are not linked to user accounts and IP addresses are not recorded. "
            "Soft anonymous: responses are linked to user accounts but not shown to survey owners. "
            "Name and email: responses are linked to user accounts and shown to survey owners."
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

    key_fields = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        verbose_name=_("key fields"),
        help_text=_("Key fields will be shown in the response list."),
    )

    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="subscribed_surveys",
        verbose_name=_("subscribers"),
        help_text=_("Users who will receive notifications when new responses are submitted."),
        blank=True,
    )

    # related fields
    dimensions: models.QuerySet[Dimension]

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
            self.languages.all().only("language", "fields"),
            key=lambda form: form.language != base_language,
        )

        return merge_fields(languages)

    def get_form(self, requested_language: str) -> Form | None:
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

        return None

    @property
    def responses(self):
        from .response import Response

        return Response.objects.filter(form__in=self.languages.all()).order_by("created_at")

    @property
    def can_remove(self):
        # TODO(#432) Revisit criteria for can_remove
        return not self.languages.exists()

    def get_next_sequence_number(self):
        return (self.responses.all().aggregate(models.Max("sequence_number"))["sequence_number__max"] or 0) + 1

    def preload_dimensions(self, dimension_values: Mapping[str, Collection[str]] | None = None):
        dimensions = self.dimensions.all().prefetch_related("values")
        if dimension_values is not None:
            dimensions = dimensions.filter(slug__in=dimension_values.keys())

        dimensions_by_slug = {dimension.slug: dimension for dimension in dimensions}

        values_by_dimension_by_slug: dict[str, dict[str, DimensionValue]] = {}
        for dimension in dimensions_by_slug.values():
            values_by_dimension_by_slug[dimension.slug] = {value.slug: value for value in dimension.values.all()}

        return dimensions_by_slug, values_by_dimension_by_slug

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return f"{self.event.slug}/{self.slug}"


@dataclass
class SurveyDTO:
    """
    A helper to ergonomically create surveys in setup scripts.

    For a survey of event tracon2024 and slug hackathon-signup that is available in English and Finnish,
    the following files should be created:
    - forms/hackathon-signup-fi.yml
    - forms/hackathon-signup-en.yml
    - an optional forms/hackathon-signup-dimensions.yml for dimensions

    If the survey already exists, its settings are not updated.
    If a language version (form) already exists, only fields are updated - other settings are not updated.
    If dimensions already exist, they are not updated.
    This is to avoid overwriting user data.
    """

    slug: str
    login_required: bool = False
    max_responses_per_user: int = 0
    anonymity: str = "soft"
    active_from: datetime = field(default_factory=now)
    key_fields: list[str] = field(default_factory=list)

    def save(self, event: Event) -> Survey:
        from .dimension import DimensionDTO

        defaults = asdict(self)  # type: ignore
        slug = defaults.pop("slug")

        survey, created = Survey.objects.get_or_create(event=event, slug=slug, defaults=defaults)
        log_get_or_create(logger, survey, created)

        if not survey.dimensions.exists():
            try:
                with resource_stream(f"events.{event.slug}", f"forms/{slug}-dimensions.yml") as f:
                    data = yaml.safe_load(f)
            except FileNotFoundError:
                pass
            else:
                dimensions = [DimensionDTO.model_validate(dimension) for dimension in data]
                DimensionDTO.save_many(survey, dimensions)

        for language in SUPPORTED_LANGUAGES:
            form_slug = f"{slug}-{language.code}"

            try:
                with resource_stream(f"events.{event.slug}", f"forms/{form_slug}.yml") as f:
                    data = yaml.safe_load(f)
            except FileNotFoundError:
                continue

            form, created = Form.objects.get_or_create(
                event=event,
                slug=form_slug,
                language=language.code,
                defaults=data,
            )
            log_get_or_create(logger, form, created)

            # TODO(#403) Remove when form editor is implemented
            if not created:
                # Update fields only on existing forms
                form.fields = data["fields"]
                form.save(update_fields=["fields"])

            survey.languages.add(form)

        return survey
