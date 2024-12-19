import graphene

from access.cbac import graphql_check_model
from core.models import Event

from ...models.product import Product
from ..product_limited import LimitedProductType


class CreateProductInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    title = graphene.String(required=True)
    description = graphene.String()
    price = graphene.Decimal()


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = CreateProductInput(required=True)

    product = graphene.Field(LimitedProductType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateProductInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Product, event.scope, info, "create")
        product = Product(
            event=event,
            title=input.title,
            description=input.description,
            price=input.price,
        )
        product.full_clean()  # Validate fields
        product.save()
        return CreateProduct(product=product)  # type: ignore
