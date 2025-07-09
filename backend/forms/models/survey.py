from __future__ import annotations

import dataclasses
import logging
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Self

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
from dimensions.models.enums import DimensionApp
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from dimensions.utils.build_cached_dimensions import build_cached_dimensions
from dimensions.utils.dimension_cache import DimensionCache
from dimensions.utils.set_dimension_values import set_dimension_values
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from involvement.models.enums import InvolvementType
from involvement.models.profile_field_selector import ProfileFieldSelector
from involvement.models.registry import Registry

from ..utils.merge_form_fields import merge_fields
from .enums import Anonymity, SurveyPurpose

if TYPE_CHECKING:
    from badges.models.survey_to_badge import SurveyToBadgeMapping

    from .form import Form
    from .survey import Survey
    from .survey_default_involvement_dimension_value import SurveyDefaultInvolvementDimensionValue
    from .survey_default_response_dimension_value import SurveyDefaultResponseDimensionValue
    from .workflow import Workflow

logger = logging.getLogger("kompassi")


class Survey(models.Model):
    event: models.ForeignKey[Event] = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="surveys")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    app_name = models.CharField(
        choices=[(app.value, app.value) for app in DimensionApp],
        max_length=max(len(app.value) for app in DimensionApp),
        default=DimensionApp.FORMS.value,
        help_text="Which app manages this survey?",
    )
    purpose_slug = models.CharField(
        choices=[(role.value, role.value) for role in SurveyPurpose],
        max_length=max(len(role.value) for role in SurveyPurpose),
        default=SurveyPurpose.DEFAULT.value,
        help_text="Generic surveys and program offers are DEFAULT, program host invitations are ACCEPT_INVITATION.",
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

    responses_editable_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("responses editable until"),
        help_text=_(
            "If set, responses to this survey can be edited by whomever sent them until this date, "
            "provided that the response is not locked by a dimension value that is set to lock subjects. "
            "If unset, responses cannnot be edited at all. "
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

    registry = models.ForeignKey(
        Registry,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="surveys",
    )

    universe = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="surveys",
    )

    default_response_dimensions: models.QuerySet[SurveyDefaultResponseDimensionValue]
    cached_default_response_dimensions = models.JSONField(blank=True, default=dict)

    default_involvement_dimensions: models.QuerySet[SurveyDefaultInvolvementDimensionValue]
    cached_default_involvement_dimensions = models.JSONField(blank=True, default=dict)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    languages: models.QuerySet[Form]
    badge_mappings: models.QuerySet[SurveyToBadgeMapping]
    id: int
    universe_id: int | None

    class Meta:
        unique_together = [("event", "slug")]

    def __init__(self, *args, **kwargs) -> None:
        if purpose := kwargs.pop("purpose", None):
            if isinstance(purpose, SurveyPurpose):
                kwargs["purpose_slug"] = purpose.value
            else:
                kwargs["purpose_slug"] = purpose

        if app := kwargs.pop("app", None):
            if isinstance(app, DimensionApp):
                kwargs["app_name"] = app.value
            else:
                kwargs["app_name"] = app

        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.event.slug}/{self.slug}"

    def save(self, **kwargs):
        self.with_mandatory_fields()
        super().save(**kwargs)

    @cached_property
    def profile_field_selector(self) -> ProfileFieldSelector:
        return ProfileFieldSelector.from_anonymity(self.anonymity)

    @property
    def app(self) -> DimensionApp:
        if not self.app_name:
            raise ValueError("app_name must be set")

        return DimensionApp(self.app_name)

    @property
    def purpose(self) -> SurveyPurpose:
        if not self.purpose_slug:
            raise ValueError("purpose_slug must be set")

        return SurveyPurpose(self.purpose_slug)

    @property
    def involvement_type(self) -> InvolvementType | None:
        # there cannot be Involvement without Registry
        if self.registry is None:
            return None

        match self.app, self.purpose:
            case DimensionApp.PROGRAM_V2, SurveyPurpose.DEFAULT:
                return InvolvementType.PROGRAM_OFFER
            case DimensionApp.PROGRAM_V2, SurveyPurpose.INVITE:
                return InvolvementType.PROGRAM_HOST
            case DimensionApp.FORMS, _:
                return InvolvementType.SURVEY_RESPONSE
            case _:
                raise NotImplementedError(f"{self.app=} {self.purpose=} is not implemented")

    @property
    def dimensions(self) -> models.QuerySet[Dimension]:
        return self.universe.dimensions.all()

    @property
    def scope(self) -> Scope:
        """
        NOTE: Used by CBAC via HasScope protocol
        """
        return self.event.scope

    def _get_universe(self) -> Universe:
        match self.app:
            case DimensionApp.FORMS:
                return Universe.objects.get_or_create(
                    scope=self.scope,
                    slug=self.slug,
                    app_name=self.app.value,
                )[0]
            case DimensionApp.PROGRAM_V2:
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

    def get_title(self, lang: str = DEFAULT_LANGUAGE) -> str | None:
        form = self.get_form(lang)
        return form.title if form is not None else None

    @property
    def current_responses(self):
        from .response import Response

        return Response.objects.filter(
            form__in=self.languages.all(),
            superseded_by=None,
        ).order_by("revision_created_at")

    @property
    def all_responses(self):
        from .response import Response

        return Response.objects.filter(
            form__in=self.languages.all(),
        ).order_by("revision_created_at")

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
                app=self.app.value,
            )
            and not self.languages.exists()
        )

    # TODO(#714) Reconcile with Workflow.can_response_be_deleted_by
    def can_responses_be_deleted_by(self, request: HttpRequest):
        return (
            is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="responses",
                app=self.app.value,
            )
            and not self.protect_responses
        )

    def get_next_sequence_number(self):
        return (self.current_responses.all().aggregate(models.Max("sequence_number"))["sequence_number__max"] or 0) + 1

    def with_mandatory_fields(self) -> Self:
        if not self.slug:
            raise ValueError("slug must be set before calling with_mandatory_fields")
        if self.app is None:
            raise ValueError("app must be set before calling with_mandatory_fields")
        if self.purpose is None:
            raise ValueError("purpose must be set before calling with_mandatory_fields")

        if self.universe_id is None:
            self.universe = self._get_universe()

        match self.app:
            case DimensionApp.PROGRAM_V2:
                meta = self.event.program_v2_event_meta
                if meta is None:
                    raise ValueError(f"Event {self.event} does not have a program v2 event meta")

                if meta.default_registry is None:
                    raise ValueError(f"Event {self.event} does not have a default registry for program v2")

                self.login_required = True
                self.anonymity = Anonymity.FULL_PROFILE
                self.registry = meta.default_registry

                if self.purpose == SurveyPurpose.DEFAULT:
                    # The program offer workflow uses a dimension to lock responses from editing.
                    self.responses_editable_until = self.event.end_time
                    self.key_fields = ["title"]

            case DimensionApp.FORMS:
                if self.purpose == SurveyPurpose.INVITE:
                    raise ValueError("ACCEPT_INVITATION is not a valid purpose for FORMS app")

                if self.anonymity == Anonymity.NAME_AND_EMAIL:
                    self.login_required = True

            case _:
                raise NotImplementedError(self.app)

        return self

    def clone(
        self,
        event: Event,
        slug: str,
        app: DimensionApp,
        purpose: SurveyPurpose,
        anonymity: Anonymity | None = None,
        created_by: AbstractBaseUser | None = None,
        registry: Registry | None = None,
    ):
        """
        Clones this survey with its language versions and dimensions (but not responses).
        Some fields are not copied over because they make no sense or might cause data leaks.
        """
        survey = Survey(
            event=event,
            slug=slug,
            app=app,
            purpose=purpose,
            anonymity=self.anonymity if anonymity is None else anonymity,
            login_required=self.login_required,
            max_responses_per_user=self.max_responses_per_user,
            key_fields=self.key_fields,
            protect_responses=self.protect_responses,
            created_by=created_by,
            registry=self.registry if registry is None else registry,
        ).with_mandatory_fields()

        survey.save()

        # TODO(#585)
        # for dimension in self.dimensions.all():
        #     dimension.clone(self.universe)

        for form in self.languages.all():
            form.clone(survey, created_by=created_by)

        return survey

    @transaction.atomic
    def set_default_response_dimension_values(
        self,
        values_to_set: Mapping[str, Collection[str]],
        cache: DimensionCache,
    ):
        from .survey_default_response_dimension_value import SurveyDefaultResponseDimensionValue

        if cache.universe.app != self.app:
            raise AssertionError(f"Expected cache universe to match survey app ({cache.universe.app} != {self.app})")

        set_dimension_values(SurveyDefaultResponseDimensionValue, self, values_to_set, cache)

    @transaction.atomic
    def set_default_involvement_dimension_values(
        self,
        values_to_set: Mapping[str, Collection[str]],
        cache: DimensionCache,
    ):
        from .survey_default_involvement_dimension_value import SurveyDefaultInvolvementDimensionValue

        if cache.universe.app != DimensionApp.INVOLVEMENT:
            raise AssertionError(f"Expected involvement dimensions cache, got {cache.universe.app}")

        set_dimension_values(SurveyDefaultInvolvementDimensionValue, self, values_to_set, cache)

    def refresh_cached_default_dimensions(self):
        self.cached_default_response_dimensions = build_cached_dimensions(self.default_response_dimensions.all())
        self.cached_default_involvement_dimensions = build_cached_dimensions(self.default_involvement_dimensions.all())
        self.save(
            update_fields=[
                "cached_default_response_dimensions",
                "cached_default_involvement_dimensions",
            ]
        )

    @classmethod
    def refresh_cached_default_dimensions_qs(
        cls,
        surveys: models.QuerySet[Survey],
        batch_size: int = 100,
    ):
        bulk_update = []
        for survey in surveys:
            survey.cached_default_response_dimensions = build_cached_dimensions(
                survey.default_response_dimensions.all()
            )
            survey.cached_default_involvement_dimensions = build_cached_dimensions(
                survey.default_involvement_dimensions.all()
            )
            bulk_update.append(survey)
        Survey.objects.bulk_update(
            bulk_update,
            [
                "cached_default_response_dimensions",
                "cached_default_involvement_dimensions",
            ],
            batch_size=batch_size,
        )


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
