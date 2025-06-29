from __future__ import annotations

import logging
from collections.abc import Collection, Mapping
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction

from badges.models import Badge
from core.models.event import Event
from core.models.person import Person
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from dimensions.utils.dimension_cache import DimensionCache
from dimensions.utils.set_dimension_values import set_dimension_values
from forms.models.survey import SurveyPurpose
from graphql_api.language import DEFAULT_LANGUAGE

from .enums import InvolvementApp, InvolvementType
from .invitation import Invitation
from .profile_field_selector import ProfileFieldSelector

if TYPE_CHECKING:
    from forms.models.response import Response
    from program_v2.models.program import Program

    from .involvement_dimension_value import InvolvementDimensionValue

from .registry import Registry

logger = logging.getLogger("kompassi")


class Involvement(models.Model):
    """
    An Involvement means a Person is somehow involved in an Event.
    This may mean eg. that they are volunteering, organizing program etc.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="involvements",
        db_index=False,
    )

    person: models.ForeignKey[Person] = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="involvements",
    )

    registry: models.ForeignKey[Registry] = models.ForeignKey(
        Registry,
        on_delete=models.CASCADE,
        related_name="involvements",
        db_index=False,
    )

    invitation: models.ForeignKey[Invitation] | None = models.ForeignKey(
        Invitation,
        help_text="Invitation that was used to create this involvement, if any.",
        on_delete=models.SET_NULL,
        related_name="involvements",
        null=True,
        blank=True,
        db_index=False,
    )

    program: models.ForeignKey[Program] | None = models.ForeignKey(
        "program_v2.Program",
        on_delete=models.CASCADE,
        related_name="involvements",
        null=True,
        blank=True,
        db_index=False,  # partial index in Meta.indexes
    )
    response: models.ForeignKey[Response] | None = models.ForeignKey(
        "forms.Response",
        on_delete=models.CASCADE,
        related_name="involvements",
        null=True,
        blank=True,
        db_index=False,  # partial index in Meta.indexes
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    cached_dimensions = models.JSONField(
        default=dict,
        blank=True,
    )

    dimensions: models.QuerySet[InvolvementDimensionValue]
    id: int
    pk: int

    class Meta:
        indexes = [
            # covers most program_v2 queries
            models.Index(fields=["universe", "person", "program", "response"]),
            # get contents of a registry
            # is this person in this registry?
            models.Index(fields=["registry", "person"]),
            models.Index(
                fields=["program"],
                condition=models.Q(program__isnull=False),
                name="involvement_program_idx",
            ),
            models.Index(
                fields=["response"],
                condition=models.Q(response__isnull=False),
                name="involvement_response_idx",
            ),
            GinIndex(
                fields=["cached_dimensions"],
                name="involvement_gin",
                opclasses=["jsonb_path_ops"],
            ),
        ]

    @cached_property
    def scope(self) -> Scope:
        return self.universe.scope

    @cached_property
    def event(self) -> Event:
        event = self.scope.event
        if event is None:
            raise ValueError(f"Scope of universe {self.universe} has no event")
        return event

    # TODO Ephemeral dimensions
    # Hoist app and type from dimensions to the Involvement table
    # but make them behave like dimensions for purposes of filtering
    @property
    def app(self) -> InvolvementApp:
        return InvolvementApp(self.cached_dimensions["app"][0])

    @property
    def type(self) -> InvolvementType:
        return InvolvementType(self.cached_dimensions["type"][0])

    @property
    def description(self) -> str:
        return f"{self.type.label}: {self.get_title() or 'No title'}"

    @property
    def profile_field_selector(self) -> ProfileFieldSelector:
        match self.type:
            case InvolvementType.PROGRAM_HOST:
                return ProfileFieldSelector.all_fields()
            case _ if self.response is not None:
                return self.response.survey.profile_field_selector
            case _:
                raise NotImplementedError(f"Profile field selector not implemented for involvement type {self.type!r}")

    @property
    def program_offer(self) -> Response | None:
        match self.type:
            case InvolvementType.PROGRAM_OFFER:
                return self.response
            case _:
                return None

    def get_title(self, lang: str = DEFAULT_LANGUAGE) -> str | None:
        match self.type:
            case InvolvementType.PROGRAM_HOST if self.program:
                return self.program.title
            case InvolvementType.PROGRAM_OFFER if self.response:
                return self.response.cached_key_fields.get("title")
            case InvolvementType.SURVEY_RESPONSE if self.response and self.response.survey:
                return self.response.survey.get_title(lang)
            case _:
                raise TypeError(f"get_title(): Invalid involvement {self.id}")

    @property
    def admin_link(self) -> str:
        match self.type:
            case InvolvementType.PROGRAM_OFFER if self.response:
                path = f"program-offers/{self.response.id}/"
            case InvolvementType.PROGRAM_HOST if self.program:
                path = f"program-admin/{self.program.slug}/hosts"
            case InvolvementType.SURVEY_RESPONSE if self.response:
                path = f"{self.response.survey.slug}/responses/{self.response.id}/"
            case _:
                raise TypeError(f"admin_link(): Invalid involvement {self.id}")

        return f"/{self.scope.slug}/{path}"

    def _build_cached_dimensions(self) -> dict[str, list[str]]:
        new_cached_dimensions = {}
        for sdv in self.dimensions.all():
            new_cached_dimensions.setdefault(sdv.value.dimension.slug, []).append(sdv.value.slug)

        return new_cached_dimensions

    @transaction.atomic
    @classmethod
    def refresh_cached_dimensions_qs(cls, queryset: models.QuerySet[Self]):
        bulk_update = []
        for obj in (
            queryset.select_for_update(of=("self",), no_key=True)
            .prefetch_related(
                "dimensions__value__dimension",
                "dimensions__value",
            )
            .only(
                "id",
                "dimensions__value__dimension__slug",
                "dimensions__value__slug",
            )
        ):
            obj.cached_dimensions = obj._build_cached_dimensions()
            bulk_update.append(obj)
        num_updated = cls.objects.bulk_update(bulk_update, ["cached_dimensions"])
        logger.info("Refreshed cached dimensions for %s involvements", num_updated)

    def refresh_cached_dimensions(self):
        self.cached_dimensions = self._build_cached_dimensions()
        self.save(update_fields=["cached_dimensions"])

    @transaction.atomic
    def set_dimension_values(self, values_to_set: Mapping[str, Collection[str]], cache: DimensionCache):
        """
        Changes only those dimension values that are present in dimension_values.

        NOTE: Caller must call refresh_cached_dimensions() or refresh_cached_dimensions_qs()
        afterwards to update the cached_dimensions field.

        :param values_to_set: Mapping of dimension slug to list of value slugs.
        :param cache: Cache from Universe.preload_dimensions()
        """
        from .involvement_dimension_value import InvolvementDimensionValue

        set_dimension_values(
            InvolvementDimensionValue,
            self,
            values_to_set,
            cache=cache,
        )

    @classmethod
    def _build_technical_dimension_values(
        cls,
        app: InvolvementApp,
        type: InvolvementType,
        is_active: bool,
    ) -> dict[str, list[str]]:
        return dict(
            app=[app.value],
            type=[type.value],
            state=is_active and ["active"] or ["inactive"],
        )

    @classmethod
    def from_survey_response(
        cls,
        response: Response,
        cache: DimensionCache,
        old_version: Response | None,
        deleting: bool = False,
    ):
        """
        Handles Involvement for normal survey responses and program offers.
        """
        if cache.universe.app != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app!r}")

        involvement_type = response.survey.involvement_type
        if involvement_type is None:
            raise ValueError(f"Survey {response.survey} does not have an involvement type")
        app = involvement_type.app

        is_active = not deleting and response.survey.workflow.is_response_active(response)
        dimensions = cls._build_technical_dimension_values(app, involvement_type, is_active)

        if old_version and deleting:
            raise AssertionError("Both old_version and deleting cannot be True at the same time")

        if old_version:
            Involvement.objects.filter(
                response=old_version,
            ).update(
                response=response,
            )

        elif deleting:
            try:
                involvement = cls.objects.get(
                    universe=cache.universe,
                    person=response.original_created_by.person,  # type: ignore
                    program=None,
                    response=response,
                )
            except cls.DoesNotExist:
                return None
            else:
                # make sure badges are revoked etc.
                involvement.is_active = is_active
                involvement.save(update_fields=["is_active"])
                involvement.set_dimension_values(dimensions, cache=cache)
                involvement.refresh_cached_dimensions()
                involvement.refresh_dependents()

                # deleting a program offer or response probably also means we want to
                # be rid of the Involvement
                involvement.delete()
                return None

        involvement, _created = cls.objects.update_or_create(
            universe=cache.universe,
            person=response.original_created_by.person,  # type: ignore
            program=None,
            response=response,
            defaults=dict(
                registry=response.survey.registry,
                is_active=is_active,
            ),
        )

        involvement.set_dimension_values(dimensions, cache=cache)
        involvement.refresh_cached_dimensions()
        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_accepted_program_offer(
        cls,
        program_offer: Response,
        program: Program,
        cache: DimensionCache,
    ):
        if cache.universe.app != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app!r}")

        app = InvolvementApp.PROGRAM
        involvement_type = InvolvementType.PROGRAM_HOST
        is_active = program.is_active

        # NOTE update_or_create for backfill
        involvement, _created = cls.objects.update_or_create(
            universe=cache.universe,
            person=program_offer.original_created_by.person,  # type: ignore
            program=program,
            defaults=dict(
                response=program_offer,
                registry=program_offer.survey.registry,
                is_active=is_active,
            ),
        )

        dimensions = cls._build_technical_dimension_values(app, involvement_type, is_active)
        involvement.set_dimension_values(dimensions, cache=cache)
        involvement.refresh_cached_dimensions()
        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_accepted_invitation(
        cls,
        invitation: Invitation,
        response: Response,
        cache: DimensionCache,
    ):
        """
        Used to accept program host invitations.
        In the future perhaps also other types of Invitations.
        """
        if cache.universe.app != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app!r}")

        if response.survey.purpose != SurveyPurpose.INVITE:
            raise ValueError(f"Expected response to be an invitation response, got {response.survey.purpose!r}")

        involvement_type = response.survey.involvement_type
        if involvement_type is None:
            raise ValueError(f"Survey {response.survey} does not have an involvement type")

        app = involvement_type.app
        is_active = response.survey.workflow.is_response_active(response)
        dimensions = cls._build_technical_dimension_values(app, involvement_type, is_active)

        involvement, _created = cls.objects.update_or_create(
            universe=cache.universe,
            person=response.original_created_by.person,  # type: ignore
            program=invitation.program,
            defaults=dict(
                response=response,
                registry=response.survey.registry,
                is_active=is_active,
                invitation=invitation,
            ),
        )

        involvement.set_dimension_values(dimensions, cache=cache)
        involvement.refresh_cached_dimensions()
        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_program_state_change(
        cls,
        program: Program,
        cache: DimensionCache,
        deleting: bool = False,
    ):
        if cache.universe.app != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app!r}")

        app = InvolvementApp.PROGRAM
        involvement_type = InvolvementType.PROGRAM_HOST
        is_active = not deleting and program.is_active
        dimensions = cls._build_technical_dimension_values(app, involvement_type, is_active)

        involvements = cls.objects.filter(
            universe=cache.universe,
            program=program,
        )

        for involvement in involvements:
            involvement.is_active = program.is_active
            involvement.save(update_fields=["is_active"])
            involvement.set_dimension_values(dimensions, cache=cache)
            involvement.refresh_cached_dimensions()
            involvement.refresh_dependents()

        if deleting:
            involvements.delete()
            return cls.objects.none()

        return involvements

    def refresh_dependents(self):
        if self.program:
            self.program.refresh_cached_fields()

        if self.event.badges_event_meta:
            Badge.ensure(self.event, self.person)
