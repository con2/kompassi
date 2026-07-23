from functools import cached_property

from kompassi.core.models.event import Event
from kompassi.core.models.person import Person
from kompassi.core.utils.model_utils import slugify
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO, DimensionValueDTO
from kompassi.dimensions.models.enums import AnnotationDataType, ValueOrdering
from kompassi.dimensions.models.universe import Universe
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.involvement.reports.combined_perks_reports import get_combined_perks_reports
from kompassi.reports.models.report import Report

from ..models.enums import INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS
from ..models.involvement import Involvement
from ..models.meta import InvolvementEventMeta


class BaseEmperkelator:
    universe: Universe
    person: Person
    existing_combined_perks: Involvement | None
    involvements: list[Involvement]

    @property
    def scope(self):
        return self.universe.scope

    @cached_property
    def event(self):
        event = self.universe.scope.event

        if event is None:
            raise ValueError("Instantiated an emperkelator on a universe with no event (this should not happen)")

        return event

    @cached_property
    def meta(self) -> InvolvementEventMeta:
        meta = self.event.involvement_event_meta

        if meta is None:
            raise ValueError(f"Event {self.event.slug} has no involvement event meta (this should not happen)")

        return meta

    @cached_property
    def cache(self):
        return self.universe.preload_dimensions()

    def __init__(
        self,
        universe: Universe,
        person: Person,
        involvements: list[Involvement],
        existing_combined_perks: Involvement | None = None,
    ):
        self.universe = universe
        self.person = person
        self.involvements = involvements
        self.existing_combined_perks = existing_combined_perks

    @classmethod
    def get_dimension_dtos(cls, event: Event) -> list[DimensionDTO]:
        """
        These dimensions will be initialized for events using this emperkelator.
        """
        dimension_dtos = []

        if event.labour_event_meta:
            dimension_dtos.append(
                DimensionDTO(
                    slug="v1-personnel-class",
                    title=dict(
                        en="Personnel class (V1)",
                        fi="Henkilöstöluokka (V1)",
                    ),
                    is_technical=True,
                    can_values_be_added=False,
                    order=-9300,
                    choices=[
                        DimensionValueDTO(
                            slug=slugify(pc.slug),
                            title=dict(fi=pc.name),
                            is_technical=True,
                        )
                        for pc in event.personnel_classes.filter(
                            app_label__in=[
                                "program_v2",
                                "labour",
                            ]
                        ).order_by("priority")
                    ],
                    value_ordering=ValueOrdering.MANUAL,
                )
            )

        return dimension_dtos

    def get_dimension_values(self) -> CachedDimensions:
        """
        These dimension values will be set on the Combined Perks Involvement.
        """
        return {}

    @classmethod
    def get_annotation_dtos(cls) -> list[AnnotationDTO]:
        dtos = [
            AnnotationDTO(
                slug="kompassi:workingHours",
                title=dict(
                    en="Working hours",
                    fi="Työtunnit",
                ),
                type=AnnotationDataType.NUMBER,
            ),
            AnnotationDTO(
                slug="internal:formattedPerks",
                title=dict(
                    en="Perks as displayed",
                    fi="Edut kuten ne näytetään",
                ),
                type=AnnotationDataType.STRING,
                is_computed=True,
                is_perk=True,
            ),
            AnnotationDTO(
                slug="internal:overrideFormattedPerks",
                title=dict(
                    en="Override perks as displayed",
                    fi="Ylikirjoita koko etulitania",
                ),
                description=dict(
                    en="If set, this will override the displayed perks",
                    fi="Jos asetettu, tämä ylikirjoittaa näytettävät edut",
                ),
                type=AnnotationDataType.STRING,
                is_perk=True,
            ),
            AnnotationDTO(
                slug="internal:overrideBadgeJobTitle",
                title=dict(
                    en="Override badge job title",
                    fi="Ylikirjoita badgeen tuleva tehtävänimike",
                ),
                description=dict(
                    en="If set, this will override the job title shown on the badge. Useful e.g. if the program organizer's badge should not show their program item title (which is normally in the title field of the involvement).",
                    fi="Jos asetettu, tämä ylikirjoittaa badgeen tulevan tehtävänimikkeen. Hyödyllinen esim. jos ohjelmanjärjestäjän badgeen ei haluta hänen ohjelmanumeronsa otsikkoa (joka normaalisti on osallistumisen otsikkokentässä).",
                ),
                type=AnnotationDataType.STRING,
                is_perk=True,
            ),
        ]

        for dto in dtos:
            dto.is_applicable_to_involvements = True
            dto.is_applicable_to_program_items = False
            dto.is_applicable_to_schedule_items = False

        return dtos

    def get_annotation_values(self) -> CachedAnnotations:
        """
        These annotations will be set on the Combined Perks Involvement.
        """
        return {}

    @classmethod
    def get_formatted_perks(cls, dimension_values: CachedDimensions, annotation_values: CachedAnnotations) -> str:
        """
        Produce the human-readable Finnish string shown at the gate, from the final
        (post-override) dimension/annotation state. Call this after manual perk
        overrides have been applied so the result reflects what is actually granted.
        """
        override = annotation_values.get("internal:overrideFormattedPerks") or ""
        if override:
            return str(override)
        return cls._format_computed_perks(dimension_values, annotation_values)

    @classmethod
    def _format_computed_perks(cls, dimension_values: CachedDimensions, annotation_values: CachedAnnotations) -> str:
        return ""

    def get_frozen_shirt_size_values(self, computed_shirt_size_values: list[str]) -> list[str]:
        """
        Freeze shirt-size dimension values after shirt order.

        - New combined perks created after freeze get no shirt.
        - Existing combined perks keep their old value, unless explicitly cleared.
        """
        if not self.meta.are_shirts_frozen():
            return computed_shirt_size_values

        if self.existing_combined_perks is None:
            return []

        existing_dimensions = self.existing_combined_perks.cached_dimensions
        existing_shirt_sizes = existing_dimensions.get("shirt-size", [])

        if not existing_shirt_sizes:
            return computed_shirt_size_values

        # Empty or explicit NONE clears shirt size even after freeze.
        if not computed_shirt_size_values or "none" in computed_shirt_size_values:
            return []

        return existing_shirt_sizes

    def get_title(self) -> str:
        return next(
            (
                involvement.title
                for involvement_type in INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS
                for involvement in self.involvements
                if involvement.type == involvement_type
            ),
            "",
        )

    @classmethod
    def get_reports(cls, event: Event, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
        return get_combined_perks_reports(event.involvement_universe, lang)
