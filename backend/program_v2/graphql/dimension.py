import graphene
from graphene_django import DjangoObjectType

from graphql_api.utils import resolve_localized_field

from ..models import (
    Dimension,
    DimensionValue,
    ProgramDimensionValue,
)


class DimensionType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = Dimension
        fields = (
            "slug",
            "values",
            "is_multi_value",
            "is_list_filter",
            "is_shown_in_detail",
            "is_negative_selection",
        )


class DimensionValueType(DjangoObjectType):
    title = graphene.String(lang=graphene.String())
    resolve_title = resolve_localized_field("title")

    class Meta:
        model = DimensionValue
        fields = (
            "slug",
            "color",
        )


class ProgramDimensionValueType(DjangoObjectType):
    class Meta:
        model = ProgramDimensionValue
        fields = ("dimension", "value")
