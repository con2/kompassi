import graphene

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.graphql.event_limited import LimitedEventType
from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.dimensions.models.enums import AnnotationFlags
from kompassi.forms.graphql.response_limited import LimitedResponseType
from kompassi.involvement.graphql.invitation_limited import LimitedInvitationType

from ..models import Program
from .program_annotation import ProgramAnnotationType
from .program_dimension_value import ProgramDimensionValueType
from .program_host_limited import LimitedProgramHostType
from .program_limited import LimitedProgramType
from .schedule_item_limited import LimitedScheduleItemType


class FullProgramType(LimitedProgramType):
    @staticmethod
    def resolve_schedule_items(program: Program, info):
        return program.schedule_items.all()

    schedule_items = graphene.NonNull(graphene.List(graphene.NonNull(LimitedScheduleItemType)))

    @staticmethod
    def resolve_annotations(
        program: Program,
        info,
        is_shown_in_detail: bool = False,
        public_only: bool = True,
    ):
        """
        Program annotation values with schema attached to them. Only public annotations are returned.

        NOTE: If querying a lot of program items, consider using cachedAnnotations instead for SPEED.
        """
        meta = program.event.program_v2_event_meta
        if meta is None:
            raise ValueError("Program without ProgramV2EventMeta, unpossible?!?")

        required_flags: AnnotationFlags = AnnotationFlags.NONE
        schema = meta.annotations_with_fallback.all()

        if public_only:
            required_flags |= AnnotationFlags.PUBLIC
        else:
            graphql_check_instance(
                program,
                info,
                field="annotations",
            )

        if is_shown_in_detail:
            required_flags |= AnnotationFlags.SHOWN_IN_DETAIL

        if required_flags != AnnotationFlags.NONE:
            schema = schema.filter(flags__has_all=required_flags)

        return [
            ProgramAnnotationType(
                annotation=annotation,  # type: ignore
                value=value,  # type: ignore
            )
            for annotation in schema
            if (value := program.annotations.get(annotation.slug, None)) not in (None, "")
        ]

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramAnnotationType)),
        description=normalize_whitespace(resolve_annotations.__doc__ or ""),
        is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
        public_only=graphene.Boolean(default_value=True),
    )

    @staticmethod
    def resolve_dimensions(
        program: Program,
        info,
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
        key_dimensions_only: bool = False,
        public_only: bool = True,
    ):
        """
        `is_list_filter` - only return dimensions that are shown in the list filter.
        `is_shown_in_detail` - only return dimensions that are shown in the detail view.
        If you supply both, you only get their intersection.
        """
        pdvs = program.dimensions.all()

        if is_list_filter:
            pdvs = pdvs.filter(value__dimension__is_list_filter=True)

        if is_shown_in_detail:
            pdvs = pdvs.filter(value__dimension__is_shown_in_detail=True)

        if key_dimensions_only:
            pdvs = pdvs.filter(value__dimension__is_key_dimension=True)

        if public_only:
            pdvs = pdvs.filter(value__dimension__is_public=True)
        else:
            graphql_check_instance(
                program,
                info,
                field="dimensions",
            )

        return pdvs.distinct()

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramDimensionValueType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        key_dimensions_only=graphene.Boolean(),
        public_only=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )

    @staticmethod
    def resolve_program_offer(program: Program, info):
        graphql_check_instance(
            program,
            info,
            field="program_offer",
        )

        return program.program_offer

    program_offer = graphene.Field(
        LimitedResponseType,
    )

    @staticmethod
    def resolve_program_hosts(
        program: Program,
        info,
        include_inactive: bool = False,
    ):
        graphql_check_instance(
            program,
            info,
            field="program_hosts",
        )

        queryset = program.involvements.filter(
            program=program,
        )

        if not include_inactive:
            queryset = queryset.filter(is_active=True)

        return queryset.select_related("person")

    program_hosts = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedProgramHostType)),
        include_inactive=graphene.Boolean(),
    )

    @staticmethod
    def resolve_invitations(program: Program, info):
        graphql_check_instance(
            program,
            info,
            field="program_hosts",
        )

        return program.invitations.filter(used_at__isnull=True)

    invitations = graphene.NonNull(graphene.List(graphene.NonNull(LimitedInvitationType)))

    event = graphene.NonNull(LimitedEventType)

    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "description",
            "cached_earliest_start_time",
            "cached_latest_end_time",
            "created_at",
            "updated_at",
            "program_offer",
            "event",
            "can_cancel",
        )
