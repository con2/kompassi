import logging
from datetime import timedelta

import graphene
from django.db import transaction
from django.utils.timezone import now

from kompassi.core.models.event import Event

from ...models.enums import ActorType
from ...models.order import Order
from ...models.order_cancellation_token import OrderCancellationToken
from ...optimized_server.models.enums import PaymentStatus, RefundType

logger = logging.getLogger(__name__)

# An emailed confirmation link can be used for this long after it was requested.
# (A new link can always be requested as long as the order remains cancellable.)
TOKEN_VALIDITY = timedelta(hours=24)


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

    Returns success=False if the order was cancelled but the provider rejected
    the refund request (order left in REFUND_FAILED for ticket sales to resolve
    with the existing admin refund tooling).

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

            if token.created_at < now() - TOKEN_VALIDITY:
                raise ValueError("The cancellation link has expired. Please request a new one.")

            order = token.order
            if not order.can_be_cancelled_by_customer():
                raise ValueError("This order can no longer be cancelled.")

            token.mark_used()

        # NOTE: cancel_and_refund manages its own transactions and performs an
        # external HTTP call to the payment provider, so it must stay outside
        # the token transaction.
        try:
            order.cancel_and_refund(
                RefundType.PROVIDER if order.cached_price > 0 else RefundType.NONE,
                actor_type=ActorType.CUSTOMER,
                actor_user=None,
            )
        except Exception:
            # If the order was left untouched, give the token back so that the
            # customer can retry with the same link instead of hitting a dead end.
            fresh_order = Order.objects.get(event=event, id=order.id)
            if fresh_order.status == PaymentStatus.PAID:
                logger.warning(
                    "Customer cancellation of order %s failed without changing the order. Restoring token.",
                    order.id,
                    exc_info=True,
                )
                token.state = "valid"
                token.used_at = None
                token.save(update_fields=["state", "used_at"])
            raise

        # The refund request may have been rejected by the provider without raising
        # (recorded as a REFUND_FAILED payment stamp). The customer must not be told
        # that the refund is on its way when it is not.
        fresh_order = Order.objects.get(event=event, id=order.id)
        refund_failed = fresh_order.status == PaymentStatus.REFUND_FAILED

        return ConfirmOrderCancellation(success=not refund_failed)  # type: ignore
