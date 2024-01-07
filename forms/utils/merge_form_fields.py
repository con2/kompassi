"""
There are multiple instances where there are multiple language versions of a form.
Usually the language versions are expected to contain the same fields, but there may
be valid instances where a language version contains fields another version doesn't.
Note that fields present in only one language version are not guaranteed to be
in any particular order.
"""

from collections.abc import Sequence, Iterable
from functools import reduce
from typing import Protocol, TypeVar, Optional

from ..models.form import Form
from ..models.field import Field


class HasSlug(Protocol):
    slug: str


T = TypeVar("T", bound=HasSlug)


def _merge_choices(
    choices: Optional[Sequence[T]],
    other_choices: Optional[Sequence[T]],
) -> Optional[list[T]]:
    if not choices:
        return list(other_choices) if other_choices else None
    if not other_choices:
        return list(choices) if choices else None

    result = {choice.slug: choice for choice in choices}
    result.update((choice.slug, choice) for choice in other_choices if choice.slug not in result)

    return list(result.values())


def _merge_fields(fields: Sequence[Field], other_fields: Sequence[Field]) -> list[Field]:
    result = {field.slug: field for field in fields}
    result.update((field.slug, field) for field in other_fields if field.slug not in result)

    for field in fields:
        if field.choices:
            result[field.slug].choices = _merge_choices(field.choices, result[field.slug].choices or [])
        if field.questions:
            result[field.slug].questions = _merge_choices(field.questions, result[field.slug].questions or [])

    return list(result.values())


def merge_fields(forms: Iterable[Form]) -> list[Field]:
    return reduce(_merge_fields, (form.validated_fields for form in forms), [])
