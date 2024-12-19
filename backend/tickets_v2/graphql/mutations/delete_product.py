import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from core.models import Event

from ...models.product import Product
from ..product_limited import LimitedProductType


class DeleteProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    product_id = graphene.Int(required=True)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        input = DeleteProductInput(required=True)

    product = graphene.Field(LimitedProductType)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteProductInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        product = Product.objects.get(event=event, id=input.product_id, superseded_by=None)
        graphql_check_instance(product, info, "self", "delete")

        # TODO can_delete
        request: HttpRequest = info.context
        if product.get_counters(request).count_reserved > 0:
            raise ValueError("Cannot delete a product of which even a single unit has been sold")

        product.delete()

        return DeleteProduct(product=product)  # type: ignore
