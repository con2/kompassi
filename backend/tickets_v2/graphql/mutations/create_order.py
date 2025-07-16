import graphene
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_model
from core.models import Event
from event_log_v2.utils.emit import emit
from graphql_api.language import DEFAULT_LANGUAGE, to_supported_language

from ...models.order import Order
from ...optimized_server.models.customer import Customer
from ...optimized_server.models.order import validate_products_dict
from ...utils.create_order import create_order
from ..order_full import FullOrderType


# NOTE: PydanticInputObjectType not used due to
# graphene_pydantic.converters.ConversionError: Don't know how to convert the Pydantic field FieldInfo(annotation=EmailStr…
class CustomerInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False, default_value="")


class OrderProductInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)


class CreateOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    language = graphene.String(required=False, default_value=DEFAULT_LANGUAGE)
    customer = graphene.InputField(CustomerInput, required=True)
    products = graphene.List(graphene.NonNull(OrderProductInput), required=True)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = CreateOrderInput(required=True)

    order = graphene.Field(FullOrderType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CreateOrderInput,
    ):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Order, event.scope, info, operation="create")

        customer = Customer.model_validate(input.customer, from_attributes=True)
        products = validate_products_dict({op.product_id: op.quantity for op in input.products})  # type: ignore
        language = to_supported_language(input.language)  # type: ignore

        print("products", products)

        order = create_order(event, customer, products, language)

        emit(
            "tickets_v2.order.created",
            event=event,
            order=order.id,
            order_number=order.formatted_order_number,
            request=request,
            context=order.admin_url,
        )

        return CreateOrder(order=order)  # type: ignore
