from graphene_django import DjangoObjectType

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
        )
