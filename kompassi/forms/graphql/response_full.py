import graphene

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
    def resolve_old_versions(response: Response, info):
        return response.old_versions.all()

    old_versions = graphene.NonNull(graphene.List(graphene.NonNull(LimitedResponseType)))
    superseded_by = graphene.Field(LimitedResponseType)

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "revision_created_at",
            "sequence_number",
            "superseded_by",
        )
