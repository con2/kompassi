import graphene
from django.http import HttpRequest

from core.models.event import Event

from ...models.order import Order
from ..order_limited import LimitedOrderType


class MarkOrderAsPaidInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)


class MarkOrderAsPaid(graphene.Mutation):
    class Arguments:
        input = MarkOrderAsPaidInput(required=True)

    order = graphene.Field(LimitedOrderType)

    @staticmethod
    def mutate(
        root,
        info,
        input: MarkOrderAsPaidInput,
    ):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)

        if not order.can_be_marked_as_paid_by(request):
            raise ValueError("Order cannot be marked as paid")

        # TODO emit

        order.mark_as_paid()

        return MarkOrderAsPaid(order=order)  # type: ignore
