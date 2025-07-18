from __future__ import annotations

import graphene
from graphene.types.generic import GenericScalar
from graphene_pydantic import PydanticObjectType

from graphql_api.utils import DEFAULT_LANGUAGE, resolve_localized_field

from ..models.reports import Column, Report, TypeOfColumn

TypeOfColumnType = graphene.Enum.from_enum(TypeOfColumn)


class ColumnType(PydanticObjectType):
    class Meta:
        model = Column
        exclude_fields = ("title",)

    type = graphene.NonNull(TypeOfColumnType)

    title = graphene.NonNull(
        graphene.String,
        lang=graphene.String(required=False, default_value=DEFAULT_LANGUAGE),
    )
    resolve_title = resolve_localized_field("title")


class ReportType(PydanticObjectType):
    class Meta:
        model = Report
        exclude_fields = ("title", "footer")

    title = graphene.NonNull(
        graphene.String,
        lang=graphene.String(required=False, default_value=DEFAULT_LANGUAGE),
    )
    resolve_title = resolve_localized_field("title")

    rows = graphene.NonNull(graphene.List(GenericScalar))
    columns = graphene.NonNull(graphene.List(graphene.NonNull(ColumnType)))

    footer = graphene.NonNull(
        graphene.String,
        lang=graphene.String(required=False, default_value=DEFAULT_LANGUAGE),
    )
    resolve_footer = resolve_localized_field("footer")
