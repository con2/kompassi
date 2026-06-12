import graphene
from django.db import transaction

from kompassi.core.models.event import Event

from ...models.enums import ActorType
from ...models.order_cancellation_token import OrderCancellationToken
from ...optimized_server.models.enums import RefundType


class ConfirmOrderCancellationInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)
    code = graphene.String(required=True)


class ConfirmOrderCancellation(graphene.Mutation):
    """
    Customer self-service cancellation, step 2 of 2: consume the one-time code
    from the confirmation email and cancel the order, initiating an automated
    refund via the payment provider if money was paid.

    May be called without authentication: the one-time code proves control of
    the email address of the order.

    If the provider refund request fails after the code is consumed, the order
    is left in REFUND_FAILED state for ticket sales to resolve with the
    existing admin refund tooling.

    NOTE: Must not return any PII (the caller may be anonymous).
    """

    class Arguments:
        input = ConfirmOrderCancellationInput(required=True)

    success = graphene.NonNull(graphene.Boolean)

    @staticmethod
    def mutate(
        _root,
        info,
        input: ConfirmOrderCancellationInput,
    ):
        event = Event.objects.get(slug=input.event_slug)

        with transaction.atomic():
            # select_for_update + state="valid" makes concurrent double submits safe:
            # the second transaction blocks here and then fails to find a valid token.
            token = OrderCancellationToken.objects.select_for_update().get(
                event=event,
                order_id=input.order_id,
                code=input.code,
                state="valid",
            )

            order = token.order
            if not order.can_be_cancelled_by_customer():
                raise ValueError("This order can no longer be cancelled.")

            token.mark_used()

        # NOTE: cancel_and_refund manages its own transactions and performs an
        # external HTTP call to the payment provider, so it must stay outside
        # the token transaction.
        order.cancel_and_refund(
            RefundType.PROVIDER if order.cached_price > 0 else RefundType.NONE,
            actor_type=ActorType.CUSTOMER,
            actor_user=None,
        )

        return ConfirmOrderCancellation(success=True)  # type: ignore
