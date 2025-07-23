import graphene
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event

from ...models.order import ActorType, Order
from ...optimized_server.models.enums import RefundType
from ..order_limited import LimitedOrderType

RefundTypeType = graphene.Enum.from_enum(RefundType)


class CancelAndRefundOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)
    refund_type = graphene.InputField(RefundTypeType, required=True)


class CancelAndRefundOrder(graphene.Mutation):
    class Arguments:
        input = CancelAndRefundOrderInput(required=True)

    order = graphene.Field(LimitedOrderType)

    # NOTE: cancel_and_refund manages its own transactions
    # @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: CancelAndRefundOrderInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)
        refund_type = RefundType(input.refund_type)
        graphql_check_instance(order, info, operation="update")

        order.cancel_and_refund(
            refund_type,
            actor_type=ActorType.ADMIN,
            actor_user=request.user,  # type: ignore
        )

        return CancelAndRefundOrder(order=order)  # type: ignore
