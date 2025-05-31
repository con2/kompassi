import graphene

from program_v2.graphql.program_limited import LimitedProgramType

from ..models.response import Response
from .form import FormType
from .response_dimension_value import ResponseDimensionValueType
from .response_limited import LimitedResponseType


class FullResponseType(LimitedResponseType):
    @staticmethod
    def resolve_form(parent: Response, info):
        return parent.form

    form = graphene.NonNull(FormType)

    @staticmethod
    def resolve_dimensions(parent: Response, info, key_dimensions_only: bool = False):
        qs = parent.dimensions.all()

        if key_dimensions_only:
            qs = qs.filter(value__dimension__is_key_dimension=True)

        return qs

    dimensions = graphene.NonNull(
        graphene.List(
            graphene.NonNull(ResponseDimensionValueType),
        ),
        key_dimensions_only=graphene.Boolean(),
    )

    @staticmethod
    def resolve_programs(parent: Response, info):
        return parent.programs.all()

    programs = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedProgramType)),
        description=(
            "If this response is a program offer, this field returns the program items created from this program offer. "
            "If this response is not to a program offer form, this will always be empty."
        ),
    )

    @staticmethod
    def resolve_old_versions(response: Response, info):
        return response.old_versions.all()

    old_versions = graphene.NonNull(graphene.List(graphene.NonNull(LimitedResponseType)))
    superseded_by = graphene.Field(LimitedResponseType)

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "created_at",
            "sequence_number",
            "superseded_by",
        )
