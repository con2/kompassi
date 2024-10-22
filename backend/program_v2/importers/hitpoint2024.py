import logging
from dataclasses import dataclass
from datetime import timedelta

from django.utils.timezone import get_current_timezone

from core.models import Event
from program_v2.models.dimension import DimensionDTO
from programme.models.programme import Programme

from .default import DefaultImporter

logger = logging.getLogger("kompassi")
tz = get_current_timezone()


@dataclass
class HitpointImporter(DefaultImporter):
    """
    May it be forever known that I resisted the urge to call this class "HitpoImporter".
    """

    event: Event
    language: str = "fi"

    date_cutoff_time = timedelta(hours=4)  # 04:00 local time

    def get_dimensions(self) -> list[DimensionDTO]:
        dimensions = super().get_dimensions()

        # remove tag dimension
        dimensions = [d for d in dimensions if d.slug != "tag"]

        # remove freeform from categories
        category_dimension = next(d for d in dimensions if d.slug == "category")
        category_dimension_choices = category_dimension.choices or []
        freeform_index = next(i for (i, d) in enumerate(category_dimension_choices or []) if d.slug == "freeform")
        if freeform_index is not None:
            category_dimension_choices.pop(freeform_index)

        # turn freeform into larp
        larp_choice = next(d for d in category_dimension_choices if d.slug == "larp")
        larp_choice.title = dict(fi="Larppaaminen", en="LARP")

        return dimensions

    def get_program_dimension_values(self, programme: Programme) -> dict[str, list[str]]:
        dimensions = super().get_program_dimension_values(programme)

        # turn freeform into larp
        category_dimension_values = set(dimensions.get("category", []))
        if "freeform" in category_dimension_values:
            category_dimension_values.remove("freeform")
            category_dimension_values.add("larp")
        # if there are other categories, remove misc
        without_misc = category_dimension_values - {"muu-ohjelma"}
        if without_misc:
            category_dimension_values = without_misc
        dimensions["category"] = list(category_dimension_values)

        return dimensions
