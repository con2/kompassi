import graphene
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event

from ...models.order import ActorType, Order
from ...optimized_server.models.enums import PaymentStatus, RefundType
from ..errors import order_errors_as_graphql_errors
from ..order_limited import LimitedOrderType

RefundTypeType = graphene.Enum.from_enum(RefundType)
PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class CancelAndRefundOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)
    refund_type = graphene.InputField(RefundTypeType, required=True)
    from_payment_status = graphene.InputField(
        PaymentStatusType,
        required=True,
        description=(
            "The order's status as last seen by the caller. If the order has since "
            "moved on to a different status, the mutation fails with error code "
            "ORDER_STATE_CHANGED rather than acting on a stale premise."
        ),
    )


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

        with order_errors_as_graphql_errors():
            order.cancel_and_refund(
                refund_type,
                from_status=PaymentStatus(input.from_payment_status),
                actor_type=ActorType.ADMIN,
                actor_user=request.user,  # type: ignore
            )

        order.refresh_from_db()
        return CancelAndRefundOrder(order=order)  # type: ignore
