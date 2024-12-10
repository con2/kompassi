import graphene
from django.http import HttpRequest
from django.urls import reverse
from graphene_django import DjangoObjectType
from graphene_pydantic import PydanticObjectType

from core.utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field

from ..models.order import Order
from ..models.receipts import Receipt
from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.models.order import OrderProduct
from ..optimized_server.utils.formatting import format_order_number

PaymentStatusType = graphene.Enum.from_enum(PaymentStatus)


class OrderProductType(PydanticObjectType):
    class Meta:
        model = OrderProduct


class ProfileOrderType(DjangoObjectType):
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

    created_at = graphene.NonNull(graphene.DateTime)
    resolve_created_at = resolve_local_datetime_field("timestamp")

    @staticmethod
    def resolve_formatted_order_number(order: Order, info):
        return format_order_number(order.order_number)

    formatted_order_number = graphene.NonNull(graphene.String)

    @staticmethod
    def resolve_total_price(order: Order, info):
        return order.cached_price

    total_price = graphene.NonNull(graphene.Decimal)

    @staticmethod
    def resolve_status(order: Order, info):
        return order.status

    status = graphene.NonNull(PaymentStatusType)

    @staticmethod
    def resolve_electronic_tickets_link(order, info):
        """
        Returns a link at which the user can view their electronic tickets.
        They need to be the owner of the order (or an admin) to access that link.
        Returns null if the order does not contain electronic tickets.
        """
        receipt = Receipt.from_order(order)
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
