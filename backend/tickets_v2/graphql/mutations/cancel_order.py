import graphene

from access.cbac import graphql_check_instance
from core.models.event import Event

from ...models.order import Order
from ..order_limited import LimitedOrderType


class CancelOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)


class CancelOrder(graphene.Mutation):
    class Arguments:
        input = CancelOrderInput(required=True)

    order = graphene.Field(LimitedOrderType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CancelOrderInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)
        graphql_check_instance(order, info, "self", "update")
        order.cancel()
        return CancelOrder(order=order)  # type: ignore
