import graphene
from django.utils.timezone import now

from kompassi.core.models.event import Event

from ...models.enums import ActorType
from ...models.order import Order
from ...models.order_cancellation_token import OrderCancellationToken


class RequestOrderCancellationInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)


class RequestOrderCancellation(graphene.Mutation):
    """
    Customer self-service cancellation, step 1 of 2: send a confirmation link
    to the email address of the order.

    May be called without authentication: possession of the order UUID is considered
    sufficient proof of being party to the order (same trust model as the anonymous
    order page), and the confirmation email closes the loop.

    NOTE: Must not return any PII (the caller may be anonymous).
    """

    class Arguments:
        input = RequestOrderCancellationInput(required=True)

    success = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def mutate(
        _root,
        info,
        input: RequestOrderCancellationInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        order = Order.objects.get(event=event, id=input.order_id)

        if not order.can_be_cancelled_by_customer():
            raise ValueError("This order cannot be cancelled.")

        # Only the most recently requested confirmation link is valid.
        OrderCancellationToken.objects.filter(
            event=event,
            order_id=order.id,
            state="valid",
        ).update(state="revoked", used_at=now())

        token = OrderCancellationToken.objects.create(
            event=event,
            order_id=order.id,
            language=order.language,
        )
        token.send()

        order.emit_event_log_entry(
            "tickets_v2.order.cancellation_requested",
            actor_type=ActorType.CUSTOMER,
        )

        return RequestOrderCancellation(success=True)  # type: ignore
