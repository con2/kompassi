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
from kompassi.labour.models.signup import Signup
from kompassi.reports.models.report import Report

from ..models.enums import INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS
from ..models.involvement import Involvement


class BaseEmperkelator:
    universe: Universe
    person: Person
    existing_combined_perks: Involvement | None
    involvements: list[Involvement]

    @property
    def scope(self):
        return self.universe.scope

    @property
    def event(self):
        return self.universe.scope.event

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

    @classmethod
    def get_dimension_values_for_legacy_signup(cls, signup: Signup):
        return {
            "v1-personnel-class": [slugify(pc.slug) for pc in signup.personnel_classes.all()],
        }

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
                    en="Override perks",
                    fi="Ylikirjoita edut",
                ),
                description=dict(
                    en="If set, this will override the displayed perks",
                    fi="Jos asetettu, tämä ylikirjoittaa näytettävät edut",
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
        return []
