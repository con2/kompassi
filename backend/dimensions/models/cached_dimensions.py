from collections.abc import Collection, Mapping
from typing import Any

from pydantic import TypeAdapter

StrictCachedDimensions = dict[str, list[str]]
CachedDimensions = Mapping[str, Collection[str]]

adapter = TypeAdapter(StrictCachedDimensions)


def validate_cached_dimensions(input: Any) -> StrictCachedDimensions:
    """
    Return the input coerced into dict[str, list[str]] or throw a ValidationError.
    Use to validate untrusted input or turn CachedDimensions into StrictCachedDimensions.
    """
    return adapter.validate_python(input)
