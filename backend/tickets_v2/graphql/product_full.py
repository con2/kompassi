import graphene
from django.http import HttpRequest

from core.utils.text_utils import normalize_whitespace

from ..models.product import Product
from .product_limited import LimitedProductType
from .quota_limited import LimitedQuotaType


class FullProductType(LimitedProductType):
    quotas = graphene.NonNull(graphene.List(graphene.NonNull(LimitedQuotaType)))

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "available_from",
            "available_until",
            "quotas",
        )

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

    @staticmethod
    def resolve_is_available(product: Product, info):
        """
        Returns true if the product can currently be sold; that is,
        if it has not been superseded and it is within its availability window.
        This does not take into account if the product has been sold out;
        for that, consult `count_available`.
        """
        return product.is_available

    is_available = graphene.NonNull(
        graphene.Boolean,
        description=normalize_whitespace(resolve_is_available.__doc__ or ""),
    )
