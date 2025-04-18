import graphene
from graphene.types.generic import GenericScalar

from core.utils.text_utils import normalize_whitespace
from forms.graphql.response_limited import LimitedResponseType

from ..models import Program
from ..models.annotations import ANNOTATIONS
from .annotations import ProgramAnnotationType
from .program_dimension_value import ProgramDimensionValueType
from .program_limited import LimitedProgramType
from .schedule_item_limited import LimitedScheduleItemType


class FullProgramType(LimitedProgramType):
    @staticmethod
    def resolve_schedule_items(program: Program, info):
        return program.schedule_items.all()

    schedule_items = graphene.NonNull(graphene.List(graphene.NonNull(LimitedScheduleItemType)))

    @staticmethod
    def resolve_annotations(program: Program, info, is_shown_in_detail: bool = False):
        """
        Program annotation values with schema attached to them. Only public annotations are returned.

        NOTE: If querying a lot of program items, consider using cachedAnnotations instead for SPEED.
        """
        annotations = [annotation for annotation in ANNOTATIONS if annotation.is_public]

        if is_shown_in_detail:
            annotations = [annotation for annotation in annotations if annotation.is_shown_in_detail]

        return [
            ProgramAnnotationType(
                annotation=annotation,  # type: ignore
                value=value,  # type: ignore
            )
            for annotation in annotations
            if (value := program.annotations.get(annotation.slug, None))
        ]

    annotations = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramAnnotationType)),
        description=normalize_whitespace(resolve_annotations.__doc__ or ""),
        is_shown_in_detail=graphene.Boolean(description="Only return annotations that are shown in the detail view."),
    )

    @staticmethod
    def resolve_dimensions(
        program: Program,
        info,
        is_list_filter: bool = False,
        is_shown_in_detail: bool = False,
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

        return pdvs.distinct()

    dimensions = graphene.NonNull(
        graphene.List(graphene.NonNull(ProgramDimensionValueType)),
        is_list_filter=graphene.Boolean(),
        is_shown_in_detail=graphene.Boolean(),
        description=normalize_whitespace(resolve_dimensions.__doc__ or ""),
    )
    cached_dimensions = graphene.Field(GenericScalar)

    color = graphene.NonNull(graphene.String)

    program_offer = graphene.Field(
        LimitedResponseType,
    )

    class Meta:
        model = Program
        fields = (
            "title",
            "slug",
            "description",
            "cached_dimensions",
            "cached_earliest_start_time",
            "cached_latest_end_time",
            "created_at",
            "updated_at",
            "program_offer",
        )
