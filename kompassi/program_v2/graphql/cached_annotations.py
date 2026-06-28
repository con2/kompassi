import graphene
from graphene.types.generic import GenericScalar

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.models.enums import AnnotationFlags

from ..models.program import Program
from ..models.schedule_item import ScheduleItem


def resolve_cached_annotations(
    subject: Program | ScheduleItem,
    info,
    is_shown_in_detail: bool = False,
    public_only: bool = True,
    slug: list[str] | None = None,
):
    """
    A mapping of program annotation slug to annotation value.
    """
    request: RequestWithCache = info.context
    meta = subject.event.program_v2_event_meta
    if meta is None:
        raise ValueError("Program without ProgramV2EventMeta, unpossible?!?")

    only_slugs = slug  # alias for clarity (TODO rename parameter in api)
    required_flags = AnnotationFlags.NONE
    schema = list(request.kompassi_cache.for_program_universe(subject.event).annotations)

    if public_only:
        required_flags |= AnnotationFlags.PUBLIC
    else:
        graphql_check_instance(
            subject,
            info,
            field="annotations",
        )

    if is_shown_in_detail:
        required_flags |= AnnotationFlags.SHOWN_IN_DETAIL

    if required_flags != AnnotationFlags.NONE:
        schema = [annotation for annotation in schema if annotation.flags & required_flags == required_flags]

    effective_annotations = subject._effective_annotations

    return {
        annotation.slug: value
        for annotation in schema
        if (value := effective_annotations.get(annotation.slug, None)) not in (None, "")
        and (only_slugs is None or annotation.slug in only_slugs)
    }


cached_annotations = graphene.NonNull(
    GenericScalar,
    description=normalize_whitespace(resolve_cached_annotations.__doc__ or ""),
    is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
    public_only=graphene.Boolean(description="Only return public annotations. Requires authorization if false."),
    slug=graphene.List(
        graphene.NonNull(graphene.String),
        description="Only return annotations with the given slugs.",
    ),
)
