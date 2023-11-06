from typing import Any, Optional
from copy import deepcopy

from core.models import Event
from program_v2.models import Dimension


def enrich_fields(fields: list[dict[str, Any]], event: Optional[Event] = None):
    return [enrich_field(field, event=event) for field in fields]


def enrich_field(field: dict[str, Any], event: Optional[Event] = None) -> dict[str, Any]:
    """
    Some field types may contain server side directives that need to be resolved before
    turning the form specification over to the frontend.
    """
    field = deepcopy(field)

    if choices_from := field.get("choicesFrom"):
        assert len(choices_from) == 1, "choicesFrom must have exactly one key: value pair"
        ((source_type, source),) = choices_from.items()
        if source_type == "dimension":
            assert event is not None, "event must be provided when choicesFrom is dimension"
            dimension = Dimension.objects.get(event=event, slug=source)
            field["choices"] = [
                dict(
                    slug=value.slug,
                    title=value.title.translate(),
                )
                for value in dimension.values.all()
            ]
        else:
            raise NotImplementedError(f"choicesFrom: {choices_from}")

        del field["choicesFrom"]

    return field
