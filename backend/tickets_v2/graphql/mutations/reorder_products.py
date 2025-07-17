import graphene
from django.db import transaction

from access.cbac import graphql_check_model
from core.models import Event

from ...models.product import Product
from ..product_limited import LimitedProductType


class ReorderProductsInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    product_ids = graphene.List(graphene.NonNull(graphene.Int), required=True)


class ReorderProducts(graphene.Mutation):
    class Arguments:
        input = ReorderProductsInput(required=True)

    products = graphene.NonNull(graphene.List(graphene.NonNull(LimitedProductType)))

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: ReorderProductsInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Product, event.scope, info, operation="update")

        if len(input.product_ids) != len(set(input.product_ids)):  # type: ignore
            raise ValueError("Duplicates in product IDs")

        products = list(
            Product.objects.filter(
                event=event,
                id__in=input.product_ids,
                superseded_by=None,
            )
        )
        if len(products) != len(input.product_ids):  # type: ignore
            raise ValueError("Some products not found")

        all_products = Product.objects.filter(event=event, superseded_by=None)
        if len(products) != all_products.count():
            raise ValueError("All products must be included when reordering")

        # plot twist: products always come in arbitrary order, not the one specified by id__in
        products_by_id = {product.id: product for product in products}
        for i, product_id in enumerate(input.product_ids, start=1):  # type: ignore
            products_by_id[int(product_id)].ordering = i * 10

        Product.objects.bulk_update(products, ["ordering"])

        return ReorderProducts(products=products)  # type: ignore
