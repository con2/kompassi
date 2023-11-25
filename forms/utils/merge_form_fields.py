"""
There are multiple instances where there are multiple language versions of a form.
Usually the language versions are expected to contain the same fields, but there may
be valid instances where a language version contains fields another version doesn't.
The aim of `merge_form_fields` is to combine the fields of multiple language versions
while trying to preserve the order of the fields.
"""

from collections.abc import Sequence
from functools import reduce
from typing import Protocol, TypeVar, Optional

from ..models.form import AbstractForm
from ..models.field import Field


class HasSlug(Protocol):
    slug: str


T = TypeVar("T", bound=HasSlug)


def _merge_into(
    lhs: Optional[Sequence[T]],
    rhs: Optional[Sequence[T]],
) -> Optional[Sequence[T]]:
    if lhs is None and rhs is not None:
        return rhs
    elif lhs is not None and rhs is None:
        return lhs
    elif lhs is None and rhs is None:
        return None

    # appease typechecker (checked above)
    assert lhs is not None
    assert rhs is not None

    lhs_index = 0
    rhs_index = 0

    result = []
    seen = set()
    lhs_priority = True

    while lhs_index < len(lhs) and rhs_index < len(rhs):
        lhs_item = lhs[lhs_index]
        rhs_item = rhs[rhs_index]

        if lhs_item.slug in seen:
            lhs_index += 1
        elif rhs_item.slug in seen:
            rhs_index += 1
        elif lhs_item.slug == rhs_item.slug:
            result.append(lhs_item)
            lhs_index += 1
            rhs_index += 1
        elif lhs_priority:
            result.append(lhs_item)
            lhs_index += 1
            lhs_priority = False
        else:
            result.append(rhs_item)
            rhs_index += 1
            lhs_priority = True

    result.extend(lhs[lhs_index:])
    result.extend(rhs[rhs_index:])
    return result


def _merge_form_fields(lhs: list[Field], rhs: list[Field]) -> list[Field]:
    result = dict()

    lhs_index = 0
    rhs_index = 0

    lhs_priority = True

    def _update_existing_field(field: Field):
        existing_field = result[field.slug]
        existing_field.choices = _merge_into(existing_field.choices, field.choices)
        existing_field.questions = _merge_into(existing_field.questions, field.questions)

    while lhs_index < len(lhs) and rhs_index < len(rhs):
        lhs_item = lhs[lhs_index]
        rhs_item = rhs[rhs_index]

        if lhs_item.slug in result:
            _update_existing_field(lhs_item)
            lhs_index += 1
        elif rhs_item.slug in result:
            _update_existing_field(rhs_item)
            rhs_index += 1
        elif lhs_item.slug == rhs_item.slug:
            result[lhs_item.slug] = lhs_item
            _update_existing_field(rhs_item)
            lhs_index += 1
            rhs_index += 1
        elif lhs_priority:
            result[lhs_item.slug] = lhs_item
            lhs_index += 1
            lhs_priority = False
        else:
            result[lhs_item.slug] = rhs_item
            rhs_index += 1
            lhs_priority = True

    while lhs_index < len(lhs):
        lhs_item = lhs[lhs_index]
        if lhs_item.slug in result:
            _update_existing_field(lhs_item)
        else:
            result[lhs_item.slug] = lhs_item
        lhs_index += 1

    while rhs_index < len(rhs):
        rhs_item = rhs[rhs_index]
        if rhs_item.slug in result:
            _update_existing_field(rhs_item)
        else:
            result[rhs_item.slug] = rhs_item
        rhs_index += 1

    return list(result.values())


def merge_form_fields(forms: Sequence[AbstractForm]) -> list[Field]:
    return reduce(_merge_form_fields, (form.validated_fields for form in forms), [])
