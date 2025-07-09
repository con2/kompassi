from collections.abc import Collection, Mapping
from typing import Annotated, Any

from pydantic import TypeAdapter
from pydantic.types import StringConstraints

Slug = Annotated[str, StringConstraints(min_length=1, pattern=r"^[a-z0-9-]+$")]
StrictCachedDimensions = dict[Slug, list[Slug]]
CachedDimensions = Mapping[str, Collection[str]]

adapter = TypeAdapter(StrictCachedDimensions)


def validate_cached_dimensions(input: Any) -> StrictCachedDimensions:
    """
    Return the input coerced into StrictCachedDimensions or throw a ValidationError.
    Use to validate untrusted input or turn CachedDimensions into StrictCachedDimensions.

    >>> validate_cached_dimensions({"dimension1": ["value1", "value2"]})
    {'dimension1': ['value1', 'value2']}
    >>> validate_cached_dimensions({"dimension1": ["value1", "value2"], "dimension2": [""]})
    ValidationError: ...
    """
    return adapter.validate_python(input)
