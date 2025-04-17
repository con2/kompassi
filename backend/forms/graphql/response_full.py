import graphene

from ..models.response import Response
from .form import FormType
from .response_dimension_value import ResponseDimensionValueType
from .response_limited import LimitedResponseType


class FullResponseType(LimitedResponseType):
    @staticmethod
    def resolve_form(parent: Response, info):
        return parent.form

    form = graphene.Field(graphene.NonNull(FormType))

    @staticmethod
    def resolve_dimensions(parent: Response, info, key_dimensions_only: bool = False):
        qs = parent.dimensions.all()

        if key_dimensions_only:
            qs = qs.filter(dimension__is_key_dimension=True)

        return qs

    dimensions = graphene.List(
        graphene.NonNull(ResponseDimensionValueType),
        key_dimensions_only=graphene.Boolean(),
    )

    class Meta:
        model = Response
        fields = (
            "id",
            "form_data",
            "created_at",
            "sequence_number",
        )
