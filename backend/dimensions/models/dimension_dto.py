from __future__ import annotations

import logging
from typing import Self

import pydantic

from .dimension import Dimension
from .dimension_value import DimensionValue
from .dimension_value_dto import DimensionValueDTO
from .enums import ValueOrdering
from .universe import Universe

logger = logging.getLogger("kompassi")


class DimensionDTO(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    slug: str = pydantic.Field(min_length=1)
    title: dict[str, str]
    order: int | None = pydantic.Field(default=None)

    is_public: bool = pydantic.Field(default=True)
    is_key_dimension: bool = pydantic.Field(default=False)
    is_multi_value: bool = pydantic.Field(default=False)
    is_list_filter: bool = pydantic.Field(default=True)
    is_shown_in_detail: bool = pydantic.Field(default=True)
    is_negative_selection: bool = pydantic.Field(default=False)
    is_technical: bool = pydantic.Field(default=False)

    value_ordering: ValueOrdering = pydantic.Field(default=ValueOrdering.TITLE)

    choices: list[DimensionValueDTO] | None = pydantic.Field(default=None)

    def save(
        self,
        universe: Universe,
        remove_other_values=False,
    ):
        return DimensionDTO.save_many(
            universe=universe,
            dimension_dtos=[self],
            remove_others=False,
            remove_other_values=remove_other_values,
        )[0]

    @classmethod
    def save_many(
        cls,
        universe: Universe,
        dimension_dtos: list[Self],
        remove_others=False,
        remove_other_values=False,
        dimension_value_batch_size=200,
        override_order: bool = False,
    ) -> list[Dimension]:
        dimensions_upsert = (
            Dimension(
                universe=universe,
                slug=dimension_dto.slug,
                # NOTE SUPPORTED_LANGUAGES
                title_en=dimension_dto.title.get("en", ""),
                title_fi=dimension_dto.title.get("fi", ""),
                title_sv=dimension_dto.title.get("sv", ""),
                is_public=dimension_dto.is_public,
                is_key_dimension=dimension_dto.is_key_dimension,
                is_multi_value=dimension_dto.is_multi_value,
                is_list_filter=dimension_dto.is_list_filter,
                is_shown_in_detail=dimension_dto.is_shown_in_detail,
                is_negative_selection=dimension_dto.is_negative_selection,
                is_technical=dimension_dto.is_technical,
                value_ordering=dimension_dto.value_ordering,
                order=dimension_dto.order if dimension_dto.order is not None else order * 10,
            )
            for order, dimension_dto in enumerate(dimension_dtos)
        )

        update_dimension_fields = [
            # NOTE SUPPORTED_LANGUAGES
            "title_en",
            "title_fi",
            "title_sv",
            "is_public",
            "is_key_dimension",
            "is_multi_value",
            "is_list_filter",
            "is_shown_in_detail",
            "is_negative_selection",
            "is_technical",
            "value_ordering",
        ]
        if override_order:
            update_dimension_fields.append("order")

        django_dimensions = Dimension.objects.bulk_create(
            dimensions_upsert,
            update_conflicts=True,
            unique_fields=(
                "universe",
                "slug",
            ),
            update_fields=update_dimension_fields,
        )
        logger.info("Saved %s dimensions in %s", len(django_dimensions), universe)

        values_upsert = (
            DimensionValue(
                dimension=dim_dj,
                slug=choice.slug,
                is_technical=choice.is_technical,
                is_subject_locked=choice.is_subject_locked,
                # NOTE SUPPORTED_LANGUAGES
                title_en=choice.title.get("en", ""),
                title_fi=choice.title.get("fi", ""),
                title_sv=choice.title.get("sv", ""),
                color=choice.color,
                order=order * 10,
            )
            for (dim_dto, dim_dj) in zip(dimension_dtos, django_dimensions, strict=True)
            for order, choice in enumerate(dim_dto.choices or [])
        )
        num_dvs = len(
            DimensionValue.objects.bulk_create(
                values_upsert,
                update_conflicts=True,
                unique_fields=("dimension", "slug"),
                update_fields=(
                    "is_technical",
                    # NOTE SUPPORTED_LANGUAGES
                    "title_en",
                    "title_fi",
                    "title_sv",
                    "color",
                    "order",
                ),
                batch_size=dimension_value_batch_size,
            )
        )
        logger.info("Saved %s dimension values in %s", num_dvs, universe)

        if remove_other_values:
            for dim_dto, dim_dj in zip(dimension_dtos, django_dimensions, strict=True):
                values_to_keep = [choice.slug for choice in dim_dto.choices or []]
                _, deleted = dim_dj.values.exclude(slug__in=values_to_keep).delete()
                logger.info("Stale dimension value cleanup for %s deleted %s", dim_dto.slug, deleted or "nothing")

        if remove_others:
            dimensions_to_keep = [dim_dto.slug for dim_dto in dimension_dtos]
            _, deleted = universe.dimensions.exclude(slug__in=dimensions_to_keep).delete()
            logger.info("Stale dimension cleanup deleted %s", deleted)

        return django_dimensions
