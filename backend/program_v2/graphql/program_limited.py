import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_local_datetime_field, resolve_localized_field, resolve_localized_field_getattr

from ..models import Program
from ..models.annotations import ANNOTATIONS
from .program_links import ProgramLink, ProgramLinkType

# imported for side effects (register object type used by django object type fields)
from .schedule_item_limited import LimitedScheduleItemType  # noqa: F401


class LimitedProgramType(DjangoObjectType):
    """
    "Limited" program items are returned when queried through ScheduleItem.program so as to
    limit DoS via deep nesting. It lacks access to `scheduleItems` which might be used to
    cause a rapid expansion of the response via deep nesting, and also lacks access to
    some fields that may be expensive to compute such as `dimensions`; however,
    `cachedDimensions` is still provided.
    """

    title = graphene.NonNull(graphene.String, lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    description = graphene.NonNull(graphene.String, lang=graphene.String())
    resolve_description = resolve_localized_field_getattr("description")

    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.annotations.get("internal:formattedHosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    resolve_location = resolve_localized_field("cached_location")

    location = graphene.String(
        description=normalize_whitespace(
            """
            Supplied for convenience. Prefer scheduleItem.location if possible.
            Caveat: When a program item has multiple schedule items, they may be in different locations.
            In such cases, a comma separated list of locations is returned.
        """
        ),
        lang=graphene.String(),
    )

    @staticmethod
    def resolve_links(
        parent: Program,
        info,
        types: list[ProgramLinkType] | None = None,
        lang=DEFAULT_LANGUAGE,
        include_expired: bool = False,
    ):
        """
        Get the links associated with the program. If types are not specified, all links are returned.
        """
        if types is None:
            types = list(ProgramLinkType)

        return [
            program_link
            for link_type in types
            if (
                program_link := ProgramLink.from_program(
                    info.context,
                    parent,
                    link_type,
                    lang,
                    include_expired=include_expired,
                )
            )
        ]

    links = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramLink)),
        description=normalize_whitespace(resolve_links.__doc__ or ""),
        types=graphene.List(ProgramLinkType),
        lang=graphene.String(),
        include_expired=graphene.Boolean(),
    )

    @staticmethod
    def resolve_cached_annotations(program: Program, info, is_shown_in_detail: bool = False):
        """
        A mapping of program annotation slug to annotation value. Only public annotations are returned.

        TODO: Provide a way to supply is_public=False annotations to the GraphQL importer.
        Perhaps make the importer authenticate?
        """
        annotations = [annotation for annotation in ANNOTATIONS if annotation.is_public]

        if is_shown_in_detail:
            annotations = [annotation for annotation in annotations if annotation.is_shown_in_detail]

        annotations_dict = {annotation.slug: annotation for annotation in annotations}

        return {
            k: v
            for (k, v) in program.annotations.items()
            if v not in (None, "") and (annotation := annotations_dict.get(k)) and annotation.is_public
        }

    cached_annotations = graphene.NonNull(
        GenericScalar,
        description=normalize_whitespace(resolve_cached_annotations.__doc__ or ""),
        is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
    )

    @staticmethod
    def resolve_color(program: Program, info):
        return program.cached_color

    color = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_is_accepting_feedback(program: Program, info, lang=DEFAULT_LANGUAGE):
        """
        A program item will only accept feedback after it has started.
        In addition, the feedback facility may be turned off for the event.
        """
        from programme.models.programme import Programme

        # TODO programme feedback is saved under V1 data model for now
        return (
            program.is_accepting_feedback
            and Programme.objects.filter(category__event=program.event_id, slug=program.slug).exists()
        )

    is_accepting_feedback = graphene.NonNull(graphene.Boolean)

    resolve_cached_earliest_start_time = resolve_local_datetime_field("cached_earliest_start_time")
    resolve_cached_latest_end_time = resolve_local_datetime_field("cached_latest_end_time")
    resolve_created_at = resolve_local_datetime_field("created_at")
    resolve_updated_at = resolve_local_datetime_field("updated_at")

    class Meta:
        model = Program
        fields = (
            "slug",
            "cached_dimensions",
            "cached_earliest_start_time",
            "cached_latest_end_time",
            "is_accepting_feedback",
            "created_at",
            "updated_at",
        )
