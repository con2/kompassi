from __future__ import annotations

from typing import Any

import pydantic


class RecipientFilterItem(pydantic.BaseModel):
    dimension: str
    values: list[str] | None = None


RecipientFilterGroup = list[RecipientFilterItem]
RecipientFilters = list[RecipientFilterGroup]

_adapter = pydantic.TypeAdapter(RecipientFilters)


def validate_recipient_filters(input: Any) -> list[list[dict[str, Any]]]:
    """
    Return recipientFilters (OR of AND-groups of {dimension, values}) coerced into
    plain JSON-serializable form, or raise pydantic.ValidationError on invalid input.
    """
    validated = _adapter.validate_python(input)
    return [[item.model_dump(exclude_none=True) for item in group] for group in validated]


def group_to_dimension_filters(group: list[dict[str, Any]]) -> dict[str, list[str]]:
    """
    Convert one AND-group of {dimension, values} items into the dict form consumed by
    DimensionFilters. A missing/empty values list means "any value" (wildcard).
    """
    return {item["dimension"]: item.get("values") or ["*"] for item in group}
