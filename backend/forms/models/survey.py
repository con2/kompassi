from __future__ import annotations

import dataclasses
import logging
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

import yaml
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from access.cbac import is_graphql_allowed_for_model
from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, is_within_period, log_get_or_create
from core.utils.pkg_resources_compat import resource_stream
from dimensions.models.dimension import Dimension
from dimensions.models.dimension_dto import DimensionDTO
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from dimensions.utils.dimension_cache import DimensionCache
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

from ..utils.merge_form_fields import merge_fields
from .enums import SurveyApp

if TYPE_CHECKING:
    from badges.models.survey_to_badge import SurveyToBadgeMapping

    from .form import Form
    from .survey_default_dimension_value import SurveyDefaultDimensionValue
    from .workflow import Workflow

logger = logging.getLogger("kompassi")


class Anonymity(models.TextChoices):
    # not linked to user account, IP address not recorded
    HARD = "HARD", _("Hard anonymous")
    # linked to user account but not shown to owner, IP address recorded
    SOFT = "SOFT", _("Soft anonymous (linked to user account but not shown to survey owner)")
    # linked to user account and shown to owner, IP address recorded
    NAME_AND_EMAIL = "NAME_AND_EMAIL", _("Name and email shown to survey owner if responded logged-in")


APP_CHOICES = [(app.value, app.value) for app in SurveyApp]


class Survey(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    app = models.CharField(
        choices=APP_CHOICES,
        max_length=max(len(k) for (k, _) in APP_CHOICES),
        default=APP_CHOICES[0][0],
        help_text="Which app manages this survey?",
    )

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
        max_length=max(len(a.value) for a in Anonymity),
        choices=Anonymity.choices,
        default=Anonymity.SOFT.value,
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
        help_text=_("The form will be available from this date onwards. If not set, the form will not be available."),
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

    protect_responses = models.BooleanField(
        default=False,
        help_text=_("If enabled, responses cannot be deleted from the UI without disabling this first."),
    )

    cached_default_dimensions = models.JSONField(blank=True, default=dict)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    languages: models.QuerySet[Form]
    badge_mappings: models.QuerySet[SurveyToBadgeMapping]
    default_dimensions: models.QuerySet[SurveyDefaultDimensionValue]
    id: int

    @property
    def dimensions(self) -> models.QuerySet[Dimension]:
        return self.universe.dimensions.all()

    @property
    def scope(self) -> Scope:
        """
        NOTE: Used by CBAC via HasScope protocol
        """
        return self.event.scope

    @cached_property
    def universe(self) -> Universe:
        match self.app:
            case "forms":
                return Universe.objects.get_or_create(
                    scope=self.scope,
                    slug=self.slug,
                    app="forms",
                )[0]
            case "program_v2":
                return self.event.program_universe
            case _:
                raise NotImplementedError(self.app)

    @cached_property
    def workflow(self) -> Workflow:
        """
        Returns the workflow for this survey. The workflow is used to
        automatically update dimensions and possibly do other things in the future.
        """
        from .workflow import Workflow

        return Workflow.get_workflow(self)

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
        See ../graphql.py:FullSurveyType.resolve_combined_fields
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
        from .form import Form

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

    @cached_property
    def title_dict(self):
        """
        Returns a dict of language code -> title for this survey.
        """
        return {form.language: form.title for form in self.languages.all()}

    def can_be_deleted_by(self, request: HttpRequest):
        return (
            is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="self",
                app=self.app,
            )
            and not self.languages.exists()
        )

    def can_responses_be_deleted_by(self, request: HttpRequest):
        return (
            is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="responses",
                app=self.app,
            )
            and not self.protect_responses
        )

    def get_next_sequence_number(self):
        return (self.responses.all().aggregate(models.Max("sequence_number"))["sequence_number__max"] or 0) + 1

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return f"{self.event.slug}/{self.slug}"

    def with_mandatory_attributes_for_app(self, app: SurveyApp):
        match app:
            case SurveyApp.PROGRAM_V2:
                self.app = "program_v2"
                self.login_required = True
                self.anonymity = Anonymity.NAME_AND_EMAIL
                self.key_fields = ["title"]
            case SurveyApp.FORMS:
                self.app = "forms"
                if self.anonymity == Anonymity.NAME_AND_EMAIL:
                    self.login_required = True

        return self

    def clone(
        self,
        event: Event,
        slug: str,
        app: SurveyApp,
        anonymity: Anonymity | None = None,
        created_by: AbstractBaseUser | None = None,
    ):
        """
        Clones this survey with its language versions and dimensions (but not responses).
        Some fields are not copied over because they make no sense or might cause data leaks.
        """
        survey = Survey(
            event=event,
            slug=slug,
            anonymity=self.anonymity if anonymity is None else anonymity,
            login_required=self.login_required,
            max_responses_per_user=self.max_responses_per_user,
            key_fields=self.key_fields,
            protect_responses=self.protect_responses,
            created_by=created_by,
        ).with_mandatory_attributes_for_app(app)

        survey.save()

        # TODO(#585)
        # for dimension in self.dimensions.all():
        #     dimension.clone(self.universe)

        for form in self.languages.all():
            form.clone(survey, created_by=created_by)

        return survey

    @transaction.atomic
    def set_default_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.
        This allows to eg. retain a technical "state" dimension while setting other values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .survey_default_dimension_value import SurveyDefaultDimensionValue

        bulk_delete = self.default_dimensions.filter(value__dimension__slug__in=values_to_set.keys())
        bulk_create: list[SurveyDefaultDimensionValue] = []

        for dimension_slug, value_slugs in values_to_set.items():
            bulk_delete = bulk_delete.exclude(
                value__dimension__slug=dimension_slug,
                value__slug__in=value_slugs,
            )

            for value_slug in value_slugs:
                if value_slug not in self.cached_default_dimensions.get(dimension_slug, []):
                    bulk_create.append(
                        SurveyDefaultDimensionValue(
                            survey=self,
                            value=cache.values_by_dimension[dimension_slug][value_slug],
                        )
                    )

        bulk_delete.delete()
        SurveyDefaultDimensionValue.objects.bulk_create(bulk_create)
        self.refresh_cached_default_dimensions()

    def _build_cached_default_dimensions(self) -> dict[str, list[str]]:
        new_cached_dimensions = {}
        for sddv in self.default_dimensions.all():
            new_cached_dimensions.setdefault(sddv.value.dimension.slug, []).append(sddv.value.slug)

        return new_cached_dimensions

    def refresh_cached_default_dimensions(self):
        self.cached_default_dimensions = self._build_cached_default_dimensions()
        self.save(update_fields=["cached_default_dimensions"])


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
    anonymity: str = "SOFT"
    key_fields: list[str] = dataclasses.field(default_factory=list)
    active_from: datetime | None = None
    active_until: datetime | None = None

    def save(self, event: Event, overwrite=False) -> Survey:
        from .form import Form

        defaults = dataclasses.asdict(self)  # type: ignore
        slug = defaults.pop("slug")

        if not overwrite and Survey.objects.filter(event=event, slug=slug).exists():
            return Survey.objects.get(event=event, slug=slug)

        survey, created = Survey.objects.update_or_create(event=event, slug=slug, defaults=defaults)
        log_get_or_create(logger, survey, created)

        try:
            with resource_stream(f"events.{event.slug}", f"forms/{slug}-dimensions.yml") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            pass
        else:
            dimensions = [DimensionDTO.model_validate(dimension) for dimension in data]
            DimensionDTO.save_many(survey.universe, dimensions)

        for language in SUPPORTED_LANGUAGES:
            try:
                with resource_stream(f"events.{event.slug}", f"forms/{slug}-{language.code}.yml") as f:
                    data = yaml.safe_load(f)
            except FileNotFoundError:
                continue

            form, created = Form.objects.update_or_create(
                event=event,
                survey=survey,
                language=language.code,
                defaults=data,
            )
            log_get_or_create(logger, form, created)

        return survey
