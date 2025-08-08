from kompassi.core.models.person import Person
from kompassi.dimensions.models.annotation_dto import AnnotationDTO
from kompassi.dimensions.models.cached_annotations import CachedAnnotations
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.enums import AnnotationDataType
from kompassi.dimensions.models.universe import Universe

from ..models.enums import INVOLVEMENT_TYPES_CONSIDERED_FOR_COMBINED_PERKS
from ..models.involvement import Involvement


class BaseEmperkelator:
    universe: Universe
    existing_combined_perks: Involvement | None
    involvements: list[Involvement]

    @property
    def scope(self):
        return self.universe.scope

    @property
    def event(self):
        return self.universe.scope.event

    def __init__(
        self,
        universe: Universe,
        person: Person,
        involvements: list[Involvement],
        existing_combined_perks: Involvement | None = None,
    ):
        self.universe = universe
        self.involvements = involvements
        self.existing_combined_perks = existing_combined_perks

    @classmethod
    def get_dimension_dtos(cls) -> list[DimensionDTO]:
        """
        These dimensions will be initialized for events using this emperkelator.
        """
        return []

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
