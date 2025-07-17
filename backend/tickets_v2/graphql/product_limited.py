import graphene
from django.db import models
from django.http import HttpRequest
from graphene_django import DjangoObjectType

from access.cbac import graphql_query_cbac_required
from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field
from tickets_v2.graphql.quota_bare import BareQuotaType

from ..models.product import Product
from ..models.quota import Quota


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

    id = graphene.NonNull(graphene.Int)

    @graphql_query_cbac_required
    @staticmethod
    def resolve_quotas(product: Product, info):
        return product.quotas.all()

    quotas = graphene.NonNull(graphene.List(BareQuotaType))

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
        Null if the product has no quotas.
        """
        request: HttpRequest = info.context
        quotas: models.QuerySet[Quota] = product.quotas.all()
        return min(
            (quota.get_counters(request).count_available for quota in quotas),
            default=None,
        )

    count_available = graphene.Int(
        description=normalize_whitespace(resolve_count_available.__doc__ or ""),
    )

    @staticmethod
    def resolve_can_delete(product: Product, info):
        """
        Returns true if the product can be deleted.
        A product can be deleted if it has not been sold at all.
        """
        request: HttpRequest = info.context
        return product.can_be_deleted_by(request)

    can_delete = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_can_delete.__doc__ or ""),
    )
