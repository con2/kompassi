from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models, transaction
from django_enum import EnumField

from kompassi.badges.models import Badge
from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.models.cached_dimensions import (
    CachedDimensions,
    StrictCachedDimensions,
    validate_cached_dimensions,
)
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.models.universe import Universe
from kompassi.dimensions.utils.build_cached_dimensions import build_cached_dimensions
from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.dimensions.utils.set_dimension_values import set_dimension_values
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.labour.models.signup import Signup

from .enums import INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS, InvolvementApp, InvolvementType, ProgramHostRole
from .invitation import Invitation
from .involvement_to_group import InvolvementToGroupMapping
from .profile_field_selector import ProfileFieldSelector

if TYPE_CHECKING:
    from kompassi.forms.models.response import Response
    from kompassi.program_v2.models.program import Program

    from .involvement_dimension_value import InvolvementDimensionValue
    from .meta import InvolvementEventMeta

from .registry import Registry

logger = logging.getLogger(__name__)


class Involvement(models.Model):
    """
    An Involvement means a Person is somehow involved in an Event.
    This may mean eg. that they are volunteering, organizing program etc.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="all_involvements",
        db_index=False,
    )

    person: models.ForeignKey[Person] = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="involvements",
    )

    app: InvolvementApp = EnumField(InvolvementApp)  # type: ignore
    type: InvolvementType = EnumField(InvolvementType)  # type: ignore

    title = models.TextField(default="")

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
    annotations = models.JSONField(
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
            models.Index(fields=["universe", "person", "app", "type"]),
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

    @property
    def description(self) -> str:
        return f"{self.type.title_en}: {self.get_title() or 'No title'}"

    @property
    def profile_field_selector(self) -> ProfileFieldSelector:
        match self.type:
            case InvolvementType.PROGRAM_HOST:
                return ProfileFieldSelector.all_fields()
            case InvolvementType.LEGACY_SIGNUP:
                return ProfileFieldSelector.all_fields()
            case InvolvementType.COMBINED_PERKS:
                # TODO in rare edge cases, might reveal information that shouldn't be
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

    @property
    def program_host_role(self) -> ProgramHostRole | None:
        match self.type:
            case InvolvementType.PROGRAM_HOST if self.invitation:
                return ProgramHostRole.INVITED
            case InvolvementType.PROGRAM_HOST:
                return ProgramHostRole.OFFERER
            case _:
                return None

    @property
    def meta(self) -> InvolvementEventMeta:
        meta = self.event.involvement_event_meta
        if meta is None:
            raise AssertionError("Involvement without InvolvementEventMeta")
        return meta

    @cached_property
    def signup(self):
        return Signup.objects.filter(event=self.event, person=self.person).first()

    def get_title(self) -> str | None:
        """
        Used to populate `title`.
        """
        match self.type:
            case InvolvementType.PROGRAM_HOST if self.program:
                return self.program.title
            case InvolvementType.PROGRAM_OFFER if self.response:
                return self.response.cached_key_fields.get("title")
            case InvolvementType.SURVEY_RESPONSE if self.response and self.response.survey:
                return self.response.form.title
            case InvolvementType.LEGACY_SIGNUP if self.signup:
                return self.signup.some_job_title
            case InvolvementType.COMBINED_PERKS:
                # up to the emperkelator, can't figure out here
                return None
            case _:
                raise TypeError(f"get_title(): Invalid involvement {self.id}")

    def with_computed_fields(self) -> Self:
        if title := self.get_title():
            self.title = title

        return self

    @property
    def admin_link(self) -> str:
        match self.type:
            case InvolvementType.PROGRAM_OFFER if self.response:
                return f"/{self.scope.slug}/program-offers/{self.response.id}/"
            case InvolvementType.PROGRAM_HOST if self.program:
                return f"/{self.scope.slug}/program-admin/{self.program.slug}/hosts"
            case InvolvementType.SURVEY_RESPONSE if self.response:
                return f"/{self.scope.slug}/{self.response.survey.slug}/responses/{self.response.id}/"
            case InvolvementType.LEGACY_SIGNUP if self.signup:
                return f"{settings.KOMPASSI_BASE_URL}/events/{self.event.slug}/labour/admin/signups/{self.person.id}/"
            case InvolvementType.COMBINED_PERKS:
                return f"/{self.scope.slug}/people/{self.person.id}"
            case _:
                raise TypeError(f"admin_link(): Invalid involvement {self.id}")

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
            obj.cached_dimensions = build_cached_dimensions(obj.dimensions.all())
            bulk_update.append(obj)
        num_updated = cls.objects.bulk_update(bulk_update, ["cached_dimensions"])
        logger.info("Refreshed cached dimensions for %s involvements", num_updated)

    def refresh_cached_dimensions(self):
        self.cached_dimensions = build_cached_dimensions(self.dimensions.all())
        self.save(update_fields=["cached_dimensions"])

    @transaction.atomic
    def set_dimension_values(self, values_to_set: CachedDimensions, cache: DimensionCache):
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
        registry: Registry,
    ) -> StrictCachedDimensions:
        return dict(
            app=[app.value],
            type=[type.value],
            state=is_active and ["active"] or ["inactive"],
            registry=[registry.slug],
        )

    def refresh_dimensions(self, dimensions_to_set: CachedDimensions | None = None, *, cache: DimensionCache):
        update_dimensions = validate_cached_dimensions(dimensions_to_set) if dimensions_to_set else {}
        update_dimensions.update(
            self._build_technical_dimension_values(self.app, self.type, self.is_active, self.registry)
        )
        self.set_dimension_values(update_dimensions, cache=cache)
        self.refresh_cached_dimensions()

    @classmethod
    def from_survey_response(
        cls,
        response: Response,
        cache: DimensionCache,
        old_version: Response | None,
        deleting: bool = False,
        override_dimensions: bool = False,
    ):
        """
        Handles Involvement for normal survey responses and program offers.
        """
        if cache.universe.app != DimensionApp.INVOLVEMENT:
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app}")

        involvement_type = response.survey.involvement_type
        if involvement_type is None:
            raise ValueError(f"Survey {response.survey} does not have an involvement type")
        app = involvement_type.app

        registry = response.survey.registry
        if registry is None:
            raise ValueError(f"Survey {response.survey} does not have a registry")

        is_active = not deleting and response.survey.workflow.is_response_active(response)

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
                involvement.with_computed_fields().save()
                involvement.refresh_dimensions(cache=cache)
                involvement.refresh_dependents()

                # deleting a program offer or response probably also means we want to
                # be rid of the Involvement
                involvement.delete()
                return None

        involvement, created = cls.objects.update_or_create(
            universe=cache.universe,
            person=response.original_created_by.person,  # type: ignore
            app=app,
            type=involvement_type,
            program=None,
            response=response,
            defaults=dict(
                registry=response.survey.registry,
                is_active=is_active,
            ),
        )

        involvement.with_computed_fields().save()

        if created or override_dimensions:
            involvement.refresh_dimensions(response.survey.cached_default_involvement_dimensions, cache=cache)
        else:
            # leave non-technical dimensions untouched
            involvement.refresh_dimensions(cache=cache)

        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_accepted_program_offer(
        cls,
        program_offer: Response,
        program: Program,
        dimension_values: CachedDimensions,
        cache: DimensionCache,
        *,
        override_dimensions: bool = False,
    ):
        if cache.universe.app != DimensionApp.INVOLVEMENT:
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app}")

        app = InvolvementApp.PROGRAM
        involvement_type = InvolvementType.PROGRAM_HOST
        is_active = program.is_active

        # NOTE update_or_create for backfill
        involvement, created = cls.objects.update_or_create(
            universe=cache.universe,
            person=program_offer.original_created_by.person,  # type: ignore
            app=app,
            type=involvement_type,
            program=program,
            defaults=dict(
                response=program_offer,
                registry=program_offer.survey.registry,
                is_active=is_active,
            ),
        )

        involvement.with_computed_fields().save()

        if created or override_dimensions:
            dimensions = validate_cached_dimensions(program_offer.survey.cached_default_involvement_dimensions)
            dimensions.update(validate_cached_dimensions(dimension_values))
            involvement.refresh_dimensions(dimensions, cache=cache)
        else:
            # leave non-technical dimensions untouched
            involvement.refresh_dimensions(cache=cache)

        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_accepted_invitation(
        cls,
        invitation: Invitation,
        response: Response,
        cache: DimensionCache,
        *,
        override_dimensions: bool = False,
    ):
        """
        Used to accept program host invitations.
        In the future perhaps also other types of Invitations.
        """
        if cache.universe.app_name != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app_name!r}")

        if response.survey.purpose != SurveyPurpose.INVITE:
            raise ValueError(f"Expected response to be an invitation response, got {response.survey.purpose!r}")

        involvement_type = response.survey.involvement_type
        if involvement_type is None or involvement_type != invitation.involvement_type:
            raise ValueError(
                f"Invitation {invitation} has involvement type {invitation.involvement_type}, "
                f"but response {response} has involvement type {involvement_type}"
            )

        registry = invitation.survey.registry
        if registry is None:
            raise ValueError(f"Invitation {invitation} does not have a registry")

        app = involvement_type.app
        is_active = response.survey.workflow.is_response_active(response)

        involvement, created = cls.objects.update_or_create(
            universe=cache.universe,
            person=response.original_created_by.person,  # type: ignore
            app=app,
            type=involvement_type,
            program=invitation.program,
            defaults=dict(
                response=response,
                registry=registry,
                is_active=is_active,
                invitation=invitation,
            ),
        )

        involvement.with_computed_fields().save()

        if created or override_dimensions:
            dimensions = validate_cached_dimensions(response.survey.cached_default_involvement_dimensions)
            dimensions.update(validate_cached_dimensions(invitation.cached_dimensions))
            involvement.refresh_dimensions(dimensions, cache=cache)
        else:
            # leave non-technical dimensions untouched
            involvement.refresh_dimensions(cache=cache)

        involvement.refresh_dependents()

        return involvement

    @classmethod
    def from_program_state_change(
        cls,
        program: Program,
        cache: DimensionCache,
        deleting: bool = False,
    ):
        if cache.universe.app_name != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app_name!r}")

        is_active = not deleting and program.is_active

        involvements = cls.objects.filter(
            universe=cache.universe,
            program=program,
            app=InvolvementApp.PROGRAM,
            type=InvolvementType.PROGRAM_HOST,
        )

        for involvement in involvements:
            involvement.is_active = is_active
            involvement.with_computed_fields().save()

            involvement.refresh_dimensions(cache=cache)
            involvement.refresh_dependents()

        if deleting:
            involvements.delete()
            return cls.objects.none()

        return involvements

    @classmethod
    def from_involvement(
        cls,
        involvement: Involvement,
        cache: DimensionCache,
        override_dimensions: bool = False,
    ) -> Self | None:
        """
        Helper to call again the from_* method that likely created the involvement.
        Used by backfill.
        """
        match involvement.type:
            case InvolvementType.COMBINED_PERKS:
                return cls.for_combined_perks(involvement.event, involvement.person)
            case InvolvementType.LEGACY_SIGNUP if involvement.signup:
                return cls.from_legacy_signup(involvement.signup)
            case InvolvementType.PROGRAM_HOST:
                # the rest of the method :)
                pass
            case _:
                raise NotImplementedError(
                    f"from_involvement() not implemented for involvement type {involvement.type!r}"
                )

        if involvement.response is None:
            raise ValueError("A program host involvement must have a response")

        if involvement.program is None:
            raise ValueError("A program host involvement must have a program")

        if involvement.invitation is not None:
            return cls.from_accepted_invitation(
                involvement.invitation,
                involvement.response,
                cache=cache,
                override_dimensions=override_dimensions,
            )

        return cls.from_accepted_program_offer(
            program_offer=involvement.response,
            program=involvement.program,
            dimension_values=involvement.cached_dimensions,
            cache=cache,
            override_dimensions=override_dimensions,
        )

    @classmethod
    def from_legacy_signup(cls, signup: Signup) -> Self | None:
        meta = signup.event.involvement_event_meta
        if meta is None:
            raise ValueError(f"Event {signup.event.slug} has no InvolvementEventMeta")

        app = InvolvementApp.VOLUNTEERS
        involvement_type = InvolvementType.LEGACY_SIGNUP

        universe = meta.universe
        existing_involvement = cls.objects.filter(
            universe=universe,
            person=signup.person,
            app=app,
            type=involvement_type,
        ).first()

        # NOTE is_alive, not is_active!
        if not signup.is_alive:
            if existing_involvement is not None:
                # We won't delete it because it may have manual overrides.
                # This way, if they are re-activated, the manual overrides are still there.
                existing_involvement.is_active = False
                existing_involvement.with_computed_fields().save()
                existing_involvement.refresh_dimensions(cache=meta.dimension_cache)
                existing_involvement.refresh_dependents()
            return existing_involvement

        involvement, _created = cls.objects.update_or_create(
            universe=universe,
            person=signup.person,
            app=app,
            type=involvement_type,
            defaults=dict(
                registry=meta.default_registry,
                is_active=True,
            ),
        )

        involvement.with_computed_fields().save()

        dimensions = {
            "v1-personnel-class": [slugify(pc.slug) for pc in signup.personnel_classes.all()],
        }

        involvement.refresh_dimensions(
            dimensions_to_set=dimensions,
            cache=meta.dimension_cache,
        )
        involvement.refresh_dependents()

        return involvement

    @classmethod
    def for_combined_perks(cls, event: Event, person: Person) -> Self | None:
        """
        Implements the Automatic Combining of Accrued Perks (ACAB), also known as Emperkelate v2.
        When a person multiclasses in an event, they may receive perks (such as free entry, meal vouchers,
        swag etc) from multiple sources. This method creates or updates an Involvement for the person in the event,
        which represents the combined perks they have accrued.

        There may be complex rules as to how these perks are combined.
        These rules may be event specific, or a generic (dumb) set of rules may be used.

        For events that print badges, this Involvement is used to determine the type of badge to print.
        """
        meta = event.involvement_event_meta
        if meta is None:
            raise ValueError(f"Event {event.slug} has no InvolvementEventMeta")

        app = InvolvementApp.INVOLVEMENT
        involvement_type = InvolvementType.COMBINED_PERKS

        universe = meta.universe
        involvements = cls.objects.filter(universe=universe, person=person)
        existing_combined_perks = involvements.filter(app=app, type=involvement_type).first()
        active_involvements = involvements.filter(is_active=True).exclude(app=app, type=involvement_type)
        Emperkelator = meta.emperkelator_class

        if Emperkelator is None or not active_involvements.exists():
            if existing_combined_perks is not None:
                # We won't delete it because it may have manual overrides.
                # This way, if they are re-activated, the manual overrides are still there.
                existing_combined_perks.is_active = False
                existing_combined_perks.with_computed_fields().save()
                existing_combined_perks.refresh_dimensions(cache=meta.dimension_cache)
                existing_combined_perks.refresh_dependents()
            return existing_combined_perks

        emperkelator = Emperkelator(
            universe=universe,
            person=person,
            involvements=list(active_involvements),
            existing_combined_perks=existing_combined_perks,
        )

        involvement, created = cls.objects.update_or_create(
            universe=universe,
            person=person,
            app=app,
            type=involvement_type,
            defaults=dict(
                registry=meta.default_registry,
                is_active=True,
                annotations=emperkelator.get_annotations(),
                title=emperkelator.get_title(),  # with_computed_fields() has no access to emperkelator
            ),
        )

        # involvement.with_computed_fields().save()

        # TODO filter out manually overridden dimensions
        dimension_values = emperkelator.get_dimensions()
        involvement.refresh_dimensions(dimension_values, cache=meta.dimension_cache)
        involvement.refresh_dependents()

        return involvement

    def refresh_dependents(self):
        if self.program:
            self.program.refresh_cached_fields()

        if self.event.badges_event_meta:
            # ITB
            Badge.ensure(self.event, self.person)

        if self.type in INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS and self.meta.emperkelator_class:
            Involvement.for_combined_perks(self.event, self.person)

        InvolvementToGroupMapping.ensure(self.universe, self.person)

    @cached_property
    def dimensions_pairs(self) -> set[tuple[str, str]]:
        """
        Returns a set of tuples (dimension_slug, value_slug) for the cached dimensions.
        """
        return {
            (dimension_slug, value_slug)
            for dimension_slug, value_slugs in self.cached_dimensions.items()
            for value_slug in value_slugs
        }
