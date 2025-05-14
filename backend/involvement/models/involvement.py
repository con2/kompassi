from __future__ import annotations

from collections.abc import Collection, Mapping
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.db import models, transaction

from core.models.event import Event
from core.models.person import Person
from dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from dimensions.utils.dimension_cache import DimensionCache

from .enums import InvolvementApp

if TYPE_CHECKING:
    from forms.models.response import Response
    from program_v2.models.program import Program

    from .involvement_dimension_value import InvolvementDimensionValue

from .registry import Registry

APP_CHOICES = [(app.value, app.label) for app in InvolvementApp]
DIMENSIONS = [
    DimensionDTO(
        slug="app",
        title=dict(
            # NOTE SUPPORTED_LANGUAGES
            en="Application",
            fi="Sovellus",
            sv="Applikation",
        ),
        is_technical=True,
        choices=[
            DimensionValueDTO(
                slug=app.value,
                # TODO SUPPORTED_LANGUAGES
                title=dict(en=app.label),
                is_technical=True,
            )
            for app in InvolvementApp
        ],
    ),
]


class Involvement(models.Model):
    """
    An Involvement means a Person is somehow involved in an Event.
    This may mean eg. that they are volunteering, organizing program etc.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="involvements",
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

    # turn these into subject_int_id and subject_uuid if there are very many
    program: models.ForeignKey[Program] = models.ForeignKey(
        "program_v2.Program",
        on_delete=models.CASCADE,
        related_name="involvements",
        null=True,
        blank=True,
        db_index=False,
    )
    response: models.ForeignKey[Response] = models.ForeignKey(
        "forms.Response",
        on_delete=models.CASCADE,
        related_name="involvements",
        null=True,
        blank=True,
        db_index=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    app_name = models.CharField(
        choices=APP_CHOICES,
        max_length=max(len(k) for (k, _) in APP_CHOICES),
    )

    cached_dimensions = models.JSONField(
        default=dict,
        blank=True,
    )

    dimensions: models.QuerySet[InvolvementDimensionValue]

    class Meta:
        indexes = [
            models.Index(fields=["universe", "person", "app_name"]),
            models.Index(fields=["registry", "person"]),
            models.Index(
                fields=["program", "person"],
                condition=models.Q(program__isnull=False),
                name="involvement_program_idx",
            ),
            models.Index(
                fields=["response", "person"],
                condition=models.Q(response__isnull=False),
                name="involvement_response_idx",
            ),
        ]

    @property
    def app(self) -> InvolvementApp:
        return InvolvementApp(self.app_name)

    @cached_property
    def scope(self) -> Scope:
        return self.universe.scope

    @cached_property
    def event(self) -> Event:
        return self.scope.event

    @property
    def description(self) -> str:
        """
        Returns a human-readable description of the involvement.
        """
        if self.app == InvolvementApp.PROGRAM:
            if self.program:
                return f"Program item: {self.program.title}"
            elif self.response:
                values, warnings = self.response.get_processed_form_data(field_slugs=["title"])
                title = values.get("title") if "title" not in warnings else None
                return f"Program offer: {title}"
        elif self.app == InvolvementApp.FORMS and self.response:
            return f"Survey response: {self.response.survey.slug}"

        return f"Unknown involvement belonging to the {self.app.label} app"

    @classmethod
    def setup_dimensions(cls, universe: Universe) -> None:
        DimensionDTO.save_many(universe, DIMENSIONS)

    @classmethod
    def get_universe(cls, event: Event) -> Universe:
        universe, created = Universe.objects.get_or_create(
            scope=event.scope,
            slug="involvement",
            app="involvement",
        )

        if created:
            cls.setup_dimensions(universe)

        return universe

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
            queryset.select_for_update(of=("self",))
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
        cls.objects.bulk_update(bulk_update, ["cached_dimensions"])

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

        bulk_delete = self.dimensions.filter(value__dimension__slug__in=values_to_set.keys())
        bulk_create: list[InvolvementDimensionValue] = []

        for dimension_slug, value_slugs in values_to_set.items():
            bulk_delete = bulk_delete.exclude(
                value__dimension__slug=dimension_slug,
                value__slug__in=value_slugs,
            )

            for value_slug in value_slugs:
                if value_slug not in self.cached_dimensions.get(dimension_slug, []):
                    bulk_create.append(
                        InvolvementDimensionValue(
                            subject=self,
                            value=cache.values_by_dimension[dimension_slug][value_slug],
                        )
                    )

        bulk_delete.delete()
        InvolvementDimensionValue.objects.bulk_create(bulk_create)

    @classmethod
    def from_survey_response(
        cls,
        response: Response,
        cache: DimensionCache,
    ):
        """
        Handles Involvement for normal survey responses and program offers.
        """
        if cache.universe.app != "involvement":
            raise ValueError(f"Expected cache to belong to involvement, got {cache.universe.app!r}")

        app = InvolvementApp.from_app_name(response.survey.app)

        involvement, _created = cls.objects.update_or_create(
            universe=cache.universe,
            person=response.created_by.person,
            program=None,
            response=response,
            app_name=app.value,
            defaults=dict(
                registry=response.survey.registry,
                is_active=response.survey.workflow.is_response_active(response),
            ),
        )

        involvement.set_dimension_values(dict(app=[app.value]), cache=cache)
        involvement.refresh_cached_dimensions()

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

        involvement, _created = cls.objects.get_or_create(
            universe=cache.universe,
            person=program_offer.created_by.person,
            program=program,
            app_name=app.value,
            defaults=dict(
                response=program_offer,
                registry=program_offer.survey.registry,
                is_active=program.is_active,
            ),
        )

        involvement.set_dimension_values(dict(app=[app.value]), cache=cache)
        involvement.refresh_cached_dimensions()

        return involvement
