import graphene

from ..models.quota import Quota
from .product_limited import LimitedProductType
from .quota_limited import LimitedQuotaType


class FullQuotaType(LimitedQuotaType):
    products = graphene.NonNull(graphene.List(graphene.NonNull(LimitedProductType)))

    class Meta:
        model = Quota
        fields = (
            "id",
            "name",
            "products",
        )

    @staticmethod
    def resolve_products(quota: Quota, info):
        return quota.products.filter(superseded_by=None)
