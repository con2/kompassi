import graphene

from kompassi.core.utils.text_utils import normalize_whitespace

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
            "max_per_order",
            "etickets_per_product",
            "created_at",
            "quotas",
            "superseded_by",
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

    @staticmethod
    def resolve_old_versions(product: Product, info):
        return Product.objects.filter(event=product.event, superseded_by=product).select_related("event")

    old_versions = graphene.NonNull(
        graphene.List(graphene.NonNull(LimitedProductType)),
        description="Old versions of this product.",
    )

    @staticmethod
    def resolve_quotas(product: Product, info):
        return product.quotas.all()

    superseded_by = graphene.Field(
        LimitedProductType,
        description="The product superseding this product, if any.",
    )
