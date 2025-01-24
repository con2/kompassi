import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from dimensions.models.dimension import Dimension
from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import resolve_localized_field_getattr

from ..models.response_dimension_value import ResponseDimensionValue
from .dimension_value import SurveyDimensionValueType


# NOTE: names may not clash with program_v2.DimensionType and program_v2.DimensionValueType
# TODO unify these
class SurveyDimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field_getattr("title")

    @staticmethod
    def resolve_can_remove(dimension: Dimension, info):
        request: HttpRequest = info.context
        return dimension.can_be_deleted_by(request)

    can_remove = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def resolve_values(
        dimension: Dimension,
        info,
        lang: str = DEFAULT_LANGUAGE,
    ):
        """
        Get values of a dimension, ordered according to the dimension's `value_ordering`.
        NOTE: In order to get the ordering in the correct language, the language needs to be provided.
        """
        return dimension.get_values(lang)

    values = graphene.NonNull(
        graphene.List(graphene.NonNull(SurveyDimensionValueType)),
        lang=graphene.String(),
    )

    class Meta:
        model = Dimension
        fields = ("slug", "values", "is_key_dimension", "is_multi_value", "is_shown_to_subject")


class ResponseDimensionValueType(DjangoObjectType):
    class Meta:
        model = ResponseDimensionValue
        fields = ("value",)

    dimension = graphene.NonNull(SurveyDimensionType)

    @staticmethod
    def resolve_dimension(rdv: ResponseDimensionValue, info):
        return rdv.value.dimension
