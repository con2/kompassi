import graphene
from django.db import transaction

from kompassi.access.cbac import graphql_check_instance
from kompassi.core.models.event import Event

from ...models.receipt import Receipt
from ...optimized_server.models.enums import ReceiptStatus
from ..order_limited import LimitedOrderType
from ..receipt_limited import LimitedReceiptType


class ResendOrderConfirmationInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    order_id = graphene.String(required=True)


class ResendOrderConfirmation(graphene.Mutation):
    class Arguments:
        input = ResendOrderConfirmationInput(required=True)

    order = graphene.Field(LimitedOrderType)
    receipt = graphene.Field(LimitedReceiptType)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: ResendOrderConfirmationInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        receipt = Receipt.objects.filter(event=event, order_id=input.order_id).latest("id")
        order = receipt.order

        graphql_check_instance(order, info, operation="update")

        receipt = Receipt(
            event_id=receipt.event_id,
            order_id=receipt.order_id,
            correlation_id=receipt.correlation_id,
            type=receipt.type,
            status=ReceiptStatus.REQUESTED,
            # current email! (not necessarily the one the original was sent to)
            email=receipt.order.email,
        )
        receipt.save()

        return ResendOrderConfirmation(order=order, receipt=receipt)  # type: ignore
