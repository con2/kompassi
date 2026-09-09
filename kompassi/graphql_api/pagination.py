from __future__ import annotations

from typing import Self

import graphene
import pydantic
from django.core.paginator import EmptyPage, Page, Paginator
from django.db import models

DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 500


class PaginationInput(pydantic.BaseModel):
    """
    Pages are numbered from 1.
    """

    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE

    @classmethod
    def from_graphql(cls, page: int | None, page_size: int | None) -> Self:
        if page is None:
            page = 1
        if page_size is None:
            page_size = DEFAULT_PAGE_SIZE

        return cls(
            page=max(page, 1),
            page_size=min(max(page_size, 1), MAX_PAGE_SIZE),
        )

    def paginate(self, queryset: models.QuerySet) -> Page:
        paginator = Paginator(queryset, self.page_size)
        try:
            return paginator.page(self.page)
        except EmptyPage:
            # A page number past the end is usually stale, left in the URL by a filter change
            # that narrowed the results. Users expect to land on the first page then, not the last.
            return paginator.page(1)


class PaginationType(graphene.ObjectType):
    page = graphene.NonNull(graphene.Int)
    page_size = graphene.NonNull(graphene.Int)
    total_count = graphene.NonNull(graphene.Int)
    total_pages = graphene.NonNull(graphene.Int)
    has_previous = graphene.NonNull(graphene.Boolean)
    has_next = graphene.NonNull(graphene.Boolean)

    @classmethod
    def from_page(cls, page: Page) -> PaginationType:
        return cls(
            page=page.number,
            page_size=page.paginator.per_page,
            total_count=page.paginator.count,
            total_pages=page.paginator.num_pages,
            has_previous=page.has_previous(),
            has_next=page.has_next(),
        )
