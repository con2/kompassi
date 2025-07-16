import graphene
from django.http import HttpRequest

from core.models.event import Event

from ...models.order import ActorType, Order
from ...optimized_server.models.enums import RefundType
from ..order_limited import LimitedOrderType

RefundTypeType = graphene.Enum.from_enum(RefundType)


class CancelOwnUnpaidOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)


class CancelOwnUnpaidOrder(graphene.Mutation):
    class Arguments:
        input = CancelOwnUnpaidOrderInput(required=True)

    order = graphene.Field(LimitedOrderType)

    # NOTE: cancel_and_refund manages its own transactions
    # @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CancelOwnUnpaidOrderInput,
    ):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)

        if not order.can_be_cancelled_by_owner(request.user):  # type: ignore
            raise Exception("You cannot cancel this order.")

        order.cancel_and_refund(
            RefundType.NONE,
            actor_type=ActorType.OWNER,
            actor_user=request.user,  # type: ignore
        )

        return CancelOwnUnpaidOrder(order=order)  # type: ignore
