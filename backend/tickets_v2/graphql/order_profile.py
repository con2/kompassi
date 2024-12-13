import graphene
from django.http import HttpRequest
from django.urls import reverse
from graphene_pydantic import PydanticObjectType

from core.graphql.event_limited import LimitedEventType
from core.utils import normalize_whitespace

from ..models.order import Order
from ..models.receipt import PendingReceipt
from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.models.order import OrderProduct
from .order_limited import LimitedOrderType

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class OrderProductType(PydanticObjectType):
    class Meta:
        model = OrderProduct


class ProfileOrderType(LimitedOrderType):
    class Meta:
        model = Order
        fields = (
            "id",
            "event",
            "order_number",
            "language",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

    event = graphene.NonNull(LimitedEventType)

    @staticmethod
    def resolve_electronic_tickets_link(order, info):
        """
        Returns a link at which the user can view their electronic tickets.
        They need to be the owner of the order (or an admin) to access that link.
        Returns null if the order does not contain electronic tickets.
        """
        receipt = PendingReceipt.from_order(order)
        if not (receipt and receipt.have_etickets):
            return None

        request: HttpRequest = info.context
        return request.build_absolute_uri(
            reverse(
                "tickets_v2:etickets_view",
                kwargs=dict(
                    event_slug=order.event.slug,
                    order_id=order.id,
                ),
            )
        )

    electronic_tickets_link = graphene.Field(
        graphene.String,
        description=normalize_whitespace(resolve_electronic_tickets_link.__doc__ or ""),
    )

    @staticmethod
    def resolve_products(order: Order, info):
        """
        Contents of the order (also known as order products or order rows).
        """
        return order.products

    products = graphene.NonNull(
        graphene.List(graphene.NonNull(OrderProductType)),
        description=normalize_whitespace(resolve_electronic_tickets_link.__doc__ or ""),
    )
