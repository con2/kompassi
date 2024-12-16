from graphene_django import DjangoObjectType

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
