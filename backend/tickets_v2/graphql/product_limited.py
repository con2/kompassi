import graphene
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field

from ..models.product import Product


class LimitedProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "available_from",
            "available_until",
            "max_per_order",
            "etickets_per_product",
            "created_at",
        )

    resolve_created_at = resolve_local_datetime_field("created_at")

    @staticmethod
    def resolve_count_paid(product: Product, info):
        """
        Computes the amount of paid units of this product.
        Other versions of this product are grouped together.
        """
        request: HttpRequest = info.context
        return product.get_counters(request).count_paid

    count_paid = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_paid.__doc__ or ""),
    )

    @staticmethod
    def resolve_count_reserved(product: Product, info):
        """
        Computes the amount of reserved units of this product.
        Other versions of this product are grouped together.
        """
        request: HttpRequest = info.context
        return product.get_counters(request).count_reserved

    count_reserved = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_reserved.__doc__ or ""),
    )

    @staticmethod
    def resolve_count_available(product: Product, info):
        """
        Computes the amount of available units of this product.
        Other versions of this product are grouped together.
        """
        request: HttpRequest = info.context
        return min(quota.get_counters(request).count_available for quota in product.quotas.all())

    count_available = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_count_available.__doc__ or ""),
    )
