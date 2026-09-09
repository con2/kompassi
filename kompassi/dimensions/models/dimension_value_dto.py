from __future__ import annotations

from typing import TYPE_CHECKING, Self

import pydantic

if TYPE_CHECKING:
    from .dimension_value import DimensionValue


class DimensionValueDTO(pydantic.BaseModel):
    slug: str
    title: dict[str, str]
    color: str = ""
    is_technical: bool = False
    is_subject_locked: bool = False

    @classmethod
    def from_dimension_value(cls, dimension_value: DimensionValue) -> Self:
        return cls(
            slug=dimension_value.slug,
            title=dimension_value.title_dict,
            color=dimension_value.color,
            is_technical=dimension_value.is_technical,
            is_subject_locked=dimension_value.is_subject_locked,
        )
