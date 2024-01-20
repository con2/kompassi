from typing import Self, TypeVar

import graphene
from django.db import models

T = TypeVar("T", bound=models.Model)


class DimensionFilterInput(graphene.InputObjectType):
    dimension = graphene.String()
    values = graphene.List(graphene.String)

    @classmethod
    def filter(cls, queryset: models.QuerySet[T], filters: list[Self] | None) -> models.QuerySet[T]:
        if filters is None:
            filters = []

        for filter in filters:
            queryset = queryset.filter(
                dimensions__dimension__slug=filter.dimension,
                dimensions__value__slug__in=filter.values,
            )

        return queryset
