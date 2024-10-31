from typing import Self, TypeVar

import graphene
from django.db import models

T = TypeVar("T", bound=models.Model)


class DimensionFilterInput(graphene.InputObjectType):
    """
    Used to construct dimension filters in GraphQL queries.
    When a list of these is present, the semantics are AND.
    For each element in the list, with respect to the values list, the semantics are OR.
    The absence of the values list, or the special value "*" in the values list, means that the dimension must exist.
    """

    dimension = graphene.NonNull(graphene.String)
    values = graphene.List(graphene.NonNull(graphene.String))

    @classmethod
    def filter(cls, queryset: models.QuerySet[T], filters: list[Self] | None) -> models.QuerySet[T]:
        if filters is None:
            filters = []

        for filter in filters:
            if filter.values is None:
                queryset = queryset.filter(dimensions__dimension__slug=filter.dimension)
            else:
                queryset = queryset.filter(
                    dimensions__dimension__slug=filter.dimension,
                    dimensions__value__slug__in=filter.values,
                )

        return queryset
