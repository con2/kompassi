import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.graphql_api.utils import get_message_in_language, resolve_local_datetime_field

from ..models import Program
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

    @staticmethod
    def resolve_cached_dimensions(parent: Program, info):
        """
        Cached dimensions are the dimension values that are set for the program item.
        This is a mapping of dimension slug to dimension value.
        """
        print("cached_dimensions", parent.cached_dimensions)
        return parent.cached_dimensions

    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_cached_hosts(parent: Program, info):
        return parent.annotations.get("internal:formattedHosts", "")

    cached_hosts = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_location(parent: Program, info, lang: str = DEFAULT_LANGUAGE):
        """
        Deprecated. Use `scheduleItem.location` instead.
        """
        first_schedule_item = parent.schedule_items.first()
        if first_schedule_item:
            return get_message_in_language(first_schedule_item.cached_location, lang)
        return ""

    location = graphene.String(
        description=normalize_whitespace(resolve_location.__doc__ or ""),
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
    def resolve_cached_annotations(
        program: Program,
        info,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
        slug: list[str] | None = None,
    ):
        """
        A mapping of program annotation slug to annotation value. Only public annotations are returned.
        """
        meta = program.event.program_v2_event_meta
        if meta is None:
            raise ValueError("Program without ProgramV2EventMeta, unpossible?!?")

        if public_only:
            schema = meta.annotations_with_fallback.filter(is_public=True)
        else:
            graphql_check_instance(
                program,
                info,
                field="annotations",
            )
            schema = meta.annotations_with_fallback.all()

        if is_shown_in_detail:
            schema = schema.filter(is_shown_in_detail=True)

        return {
            annotation.slug: value
            for annotation in schema
            if (value := program.annotations.get(annotation.slug, None)) not in (None, "")
            and (slug is None or annotation.slug in slug)
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
        from kompassi.zombies.programme.models.programme import Programme

        # TODO programme feedback is saved under V1 data model for now
        return (
            program.is_accepting_feedback
            and Programme.objects.filter(category__event=program.event_id, slug=program.slug).exists()
        )

    is_accepting_feedback = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_is_cancelled(program: Program, info):
        return program.is_cancelled

    is_cancelled = graphene.NonNull(graphene.Boolean)

    resolve_cached_earliest_start_time = resolve_local_datetime_field("cached_earliest_start_time")
    resolve_cached_latest_end_time = resolve_local_datetime_field("cached_latest_end_time")
    resolve_created_at = resolve_local_datetime_field("created_at")
    resolve_updated_at = resolve_local_datetime_field("updated_at")

    @staticmethod
    def resolve_can_cancel(program: Program, info):
        return program.can_be_cancelled_by(info.context)

    can_cancel = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_can_delete(program: Program, info):
        return program.can_be_deleted_by(info.context)

    can_delete = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_can_restore(program: Program, info):
        return program.can_be_restored_by(info.context)

    can_restore = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_can_invite_program_host(program: Program, info):
        return program.can_program_host_be_invited_by(info.context)

    can_invite_program_host = graphene.NonNull(graphene.Boolean)

    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "description",
            "cached_dimensions",
            "cached_earliest_start_time",
            "cached_latest_end_time",
            "is_accepting_feedback",
            "created_at",
            "updated_at",
        )
