import graphene
from django.http import HttpRequest

from kompassi.core.models.event import Event

from ...models.order import ActorType, Order
from ...optimized_server.models.enums import PaymentStatus
from ..order_limited import LimitedOrderType

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class FulfilOrderInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)
    from_payment_status = graphene.InputField(
        PaymentStatusType,
        required=True,
        description=(
            "The order's status as last seen by the caller. If the order has since "
            "moved on to a different status, the mutation fails with OrderStateChanged "
            "rather than acting on a stale premise."
        ),
    )


class FulfilOrder(graphene.Mutation):
    """
    Ensures the order holds its expected tickets — minting into the quota
    whatever is missing — and records it as paid. For an order that already
    holds its tickets (the common case) this is today's "mark as paid". For
    an order flagged PAID_AFTER_CANCELLATION this is the admin's "make it so":
    the order's tickets are minted into the quota, oversold by exactly the
    amount owed, and the customer receives their receipt and e-tickets.
    """

    class Arguments:
        input = FulfilOrderInput(required=True)

    order = graphene.Field(LimitedOrderType)

    @staticmethod
    def mutate(
        root,
        info,
        input: FulfilOrderInput,
    ):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)

        if not order.can_be_fulfilled_by(request):
            raise ValueError("Order cannot be fulfilled")

        order.fulfil(
            from_status=PaymentStatus(input.from_payment_status),
            actor_type=ActorType.ADMIN,
            actor_user=request.user,  # type: ignore
        )

        return FulfilOrder(order=order)  # type: ignore
