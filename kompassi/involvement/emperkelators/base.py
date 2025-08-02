from kompassi.core.models.person import Person
from kompassi.dimensions.models.cached_dimensions import CachedDimensions
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.universe import Universe
from kompassi.program_v2.models.cached_annotations import CachedAnnotations

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

    def get_dimensions(self) -> CachedDimensions:
        return {}

    def get_annotations(self) -> CachedAnnotations:
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
